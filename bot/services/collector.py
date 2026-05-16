from datetime import datetime
from bot.database import get_db_connection


def log_update(user_id: int, chat_id: int, is_command: bool):
	conn = get_db_connection()
	c = conn.cursor()
	timestamp = datetime.now().isoformat()

	c.execute("""
        INSERT INTO updates (timestamp, user_id, chat_id, is_command)
        VALUES (?, ?, ?, ?)
    """, (timestamp, user_id, chat_id, int(is_command)))

	conn.commit()
	conn.close()