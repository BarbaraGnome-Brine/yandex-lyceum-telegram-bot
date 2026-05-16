import sqlite3
import os
from bot.config import settings

# Data folder
os.makedirs(os.path.dirname(settings.database.path), exist_ok=True)


def get_db_connection():
	conn = sqlite3.connect(settings.database.path)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA journal_mode=WAL")
	return conn


def init_db():
	conn = get_db_connection()
	c = conn.cursor()

	c.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            is_command INTEGER DEFAULT 0
        )
    """)

	c.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            detected_at TEXT NOT NULL,
            type TEXT DEFAULT 'unknown'
        )
    """)

	# Persistent user language settings
	c.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            language_code TEXT NOT NULL DEFAULT 'ru',
            updated_at TEXT NOT NULL
        )
    """)

	# Tracking warnings per user per group
	c.execute("""
        CREATE TABLE IF NOT EXISTS user_warns (
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            warn_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, chat_id)
        )
    """)

	c.execute("""
            CREATE TABLE IF NOT EXISTS alert_cooldowns (
                user_id INTEGER,
                chat_id INTEGER,
                last_alert_at TEXT,
                PRIMARY KEY (user_id, chat_id)
            )
        """)
	conn.commit()
	conn.close()


def set_user_language(user_id: int, lang_code: str):
	from datetime import datetime
	conn = get_db_connection()
	c = conn.cursor()
	c.execute("""
        INSERT INTO user_settings (user_id, language_code, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            language_code = excluded.language_code,
            updated_at = excluded.updated_at
    """, (user_id, lang_code, datetime.now().isoformat()))
	conn.commit()
	conn.close()


def get_user_language(user_id: int):
	conn = get_db_connection()
	c = conn.cursor()
	c.execute("SELECT language_code FROM user_settings WHERE user_id = ?", (user_id,))
	row = c.fetchone()
	conn.close()
	return row['language_code'] if row else None


def add_warning(user_id: int, chat_id: int) -> int:
	conn = get_db_connection()
	c = conn.cursor()
	c.execute("""
        INSERT INTO user_warns (user_id, chat_id, warn_count)
        VALUES (?, ?, 1)
        ON CONFLICT(user_id, chat_id) DO UPDATE SET
            warn_count = warn_count + 1
    """, (user_id, chat_id))
	c.execute("SELECT warn_count FROM user_warns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
	count = c.fetchone()[0]
	conn.commit()
	conn.close()
	return count


def reset_warnings(user_id: int, chat_id: int):
	conn = get_db_connection()
	c = conn.cursor()
	c.execute("DELETE FROM user_warns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
	conn.commit()
	conn.close()


def can_send_alert(user_id: int, chat_id: int, cooldown_minutes: int) -> bool:
	from datetime import datetime, timedelta
	conn = get_db_connection()
	c = conn.cursor()
	c.execute("SELECT last_alert_at FROM alert_cooldowns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
	row = c.fetchone()

	if not row:
		conn.close()
		return True

	last_alert = datetime.fromisoformat(row['last_alert_at'])
	if datetime.now() > last_alert + timedelta(minutes=cooldown_minutes):
		conn.close()
		return True

	conn.close()
	return False


def update_alert_timestamp(user_id: int, chat_id: int):
	from datetime import datetime
	conn = get_db_connection()
	conn.execute("""
        INSERT INTO alert_cooldowns (user_id, chat_id, last_alert_at)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, chat_id) DO UPDATE SET last_alert_at = excluded.last_alert_at
    """, (user_id, chat_id, datetime.now().isoformat()))
	conn.commit()
	conn.close()


init_db()


def get_daily_chat_stats():
	from datetime import datetime, timedelta

	conn = get_db_connection()
	c = conn.cursor()

	yesterday = (datetime.now() - timedelta(days=1)).isoformat()

	c.execute("""
        SELECT chat_id, COUNT(id) as msg_count, COUNT(DISTINCT user_id) as user_count 
        FROM updates 
        WHERE timestamp > ? 
        GROUP BY chat_id
    """, (yesterday,))
	updates_data = c.fetchall()

	c.execute("""
        SELECT chat_id, COUNT(id) as anomaly_count 
        FROM anomalies 
        WHERE detected_at > ? 
        GROUP BY chat_id
    """, (yesterday,))
	anomalies_data = {row['chat_id']: row['anomaly_count'] for row in c.fetchall()}

	conn.close()

	stats = {}
	for row in updates_data:
		chat_id = row['chat_id']
		stats[chat_id] = {
			'messages': row['msg_count'],
			'users': row['user_count'],
			'anomalies': anomalies_data.get(chat_id, 0)
		}

	return stats
