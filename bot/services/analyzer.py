from datetime import datetime, timedelta

from bot.config import settings
from bot.database import get_db_connection


# check_for_anomalies
def check_for_anomalies(user_id: int, chat_id: int) -> bool:
	conn = get_db_connection()
	c = conn.cursor()

	time_window = datetime.now() - timedelta(seconds=60)

	c.execute(
		"SELECT COUNT(*) FROM updates "
		"WHERE user_id = ? AND chat_id = ? AND timestamp > ?",
		(user_id, chat_id, time_window.isoformat())
	)

	count = c.fetchone()[0]

	if count > settings.monitoring.anomaly_threshold:
		c.execute(
			"INSERT INTO anomalies (user_id, chat_id, detected_at, type) "
			"VALUES (?, ?, ?, ?)",
			(user_id, chat_id, datetime.now().isoformat(), "high_frequency_spam")
		)
		conn.commit()
		conn.close()
		return True

	conn.close()
	return False
