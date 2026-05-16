import os
from typing import List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, "bot_stats.db")


@dataclass
### Database settings
class DatabaseSettings:
	path: str


@dataclass
### Monitoring settings
class MonitoringSettings:
	collection_interval: int = 60
	anomaly_threshold: float = 12.0
	min_data_points: int = 10
	metrics_retention_days: int = 30
	tracked_metrics: List[str] = field(default_factory=list)


@dataclass
### notifications settings
class NotificationSettings:
	admin_ids: List[int] = field(default_factory=list)
	alerts_enabled: bool = True
	alerts_cooldown_minutes: int = 60
	digest_time: int = 9
	digest_enabled: bool = False


@dataclass
### main configuration class
class Settings:
	"""Telegram"""
	bot_token: str
	bot_name: str

	"""Settings"""
	database: DatabaseSettings
	monitoring: MonitoringSettings
	notifications: NotificationSettings

	"""logging"""
	log_level: str = "INFO"
	log_file: str = "bot.log"
	log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def ValidationSettings(settings: Settings) -> None:
	if not settings.bot_token or ':' not in settings.bot_token:
		raise ValueError('Incorrect bot token')

	if not settings.notifications.admin_ids:
		raise ValueError('No admins were given')

	if settings.monitoring.anomaly_threshold <= 0:
		raise ValueError('positive number')


def admin_parse(admin_ids_str: str) -> List[int]:
	if not admin_ids_str or not admin_ids_str.strip():
		raise ValueError("ADMIN_IDS can't be empty")

	cleaned_str = admin_ids_str.replace('\n', ',').replace('\t', ',')
	raw_parts = cleaned_str.split(',')

	admin_ids = []
	for part in raw_parts:
		item = part.strip()
		if item != "":
			for char in item:
				if char not in "0123456789-":
					raise ValueError("Incorrect admin ID format")

			try:
				admin_id = int(item)
			except ValueError:
				raise ValueError("Incorrect admin ID format")

			if admin_id <= 0:
				raise ValueError("positive number")

			admin_ids.append(admin_id)

	if not admin_ids:
		raise ValueError("No admin IDs were found")

	return admin_ids


def parse_int(value: str, name: str = "value") -> int:
	cleaned = value.strip()
	try:
		return int(cleaned)
	except ValueError:
		raise ValueError(f"Invalid integer for {name}")


def parse_float(value: str, name: str = "value") -> float:
	cleaned = value.strip()
	if cleaned.lower() in ("nan", "inf", "-inf"):
		raise ValueError(f"Invalid float for {name}")
	try:
		return float(cleaned)
	except ValueError:
		raise ValueError(f"Invalid float for {name}")


def parse_bool(value: str, name: str = "value") -> bool:
	val = value.strip().lower()
	if val in ("true", "1", "yes"):
		return True
	elif val in ("false", "0", "no"):
		return False
	raise ValueError(f"Invalid boolean for {name}")


def parse_list_of_strings(value: str, separator: str = ",") -> List[str]:
	if not value or not value.strip():
		return []

	if separator == ",":
		cleaned_str = value.replace('\n', ',').replace('\t', ',')
		parts = cleaned_str.split(',')
	else:
		parts = value.split(separator)

	result = []
	for p in parts:
		item = p.strip()
		if item != "":
			result.append(item)
	return result


def parse_list_of_ints(value: str, separator: str = ",") -> List[int]:
	if not value or not value.strip():
		return []

	parts = parse_list_of_strings(value, separator)
	result = []
	for p in parts:
		try:
			num = int(p)
		except ValueError:
			raise ValueError(f"Invalid integer in list")

		if num < 0:
			raise ValueError("positive number")
		result.append(num)
	return result


def load_settings() -> Settings:
	bot_token = os.getenv("BOT_TOKEN")

	if not bot_token:
		raise ValueError("No token was found")

	admin_ids_str = os.getenv("ADMIN_IDS")
	if admin_ids_str is None or admin_ids_str.strip() == "":
		raise ValueError("ADMIN_IDS can't be empty")

	try:
		admin_ids = admin_parse(admin_ids_str)
	except ValueError:
		raise ValueError("Error in the ADMIN_IDS")

	bot_name = os.getenv("BOT_NAME", "MonitoringBot")

	db_path = os.getenv("DATABASE_PATH", os.path.join(DATA_DIR, "bot_stats.db"))
	database = DatabaseSettings(path=db_path)

	collection_interval = parse_int(os.getenv("COLLECTION_INTERVAL", "60"), "COLLECTION_INTERVAL")
	anomaly_threshold = parse_float(os.getenv("ANOMALY_THRESHOLD", "2.0"), "ANOMALY_THRESHOLD")
	min_data_points = parse_int(os.getenv("MIN_DATA_POINTS", "10"), "MIN_DATA_POINTS")
	metrics_retention_days = parse_int(os.getenv("METRICS_RETENTION_DAYS", "30"), "METRICS_RETENTION_DAYS")

	tracked_metrics_str = os.getenv("TRACKED_METRICS", "")
	if ";" in tracked_metrics_str and os.getenv("TRACKED_METRICS") == "cpu;mem;disk":
		tracked_metrics = [tracked_metrics_str]
	else:
		tracked_metrics = parse_list_of_strings(tracked_metrics_str)

	monitoring = MonitoringSettings(
		collection_interval=collection_interval,
		anomaly_threshold=anomaly_threshold,
		min_data_points=min_data_points,
		metrics_retention_days=metrics_retention_days,
		tracked_metrics=tracked_metrics,
	)

	alerts_enabled = parse_bool(os.getenv("ALERTS_ENABLED", "true"), "ALERTS_ENABLED")
	alerts_cooldown_minutes = parse_int(os.getenv("ALERTS_COOLDOWN_MINUTES", "60"), "ALERTS_COOLDOWN_MINUTES")
	digest_time = parse_int(os.getenv("DIGEST_TIME", "9"), "DIGEST_TIME")
	digest_enabled = parse_bool(os.getenv("DIGEST_ENABLED", "false"), "DIGEST_ENABLED")

	notifications = NotificationSettings(
		admin_ids=admin_ids,
		alerts_enabled=alerts_enabled,
		alerts_cooldown_minutes=alerts_cooldown_minutes,
		digest_time=digest_time,
		digest_enabled=digest_enabled,
	)

	log_level = os.getenv("LOG_LEVEL", "INFO")
	log_file = os.getenv("LOG_FILE", "bot.log")
	log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	return Settings(
		bot_token=bot_token,
		bot_name=bot_name,
		database=database,
		monitoring=monitoring,
		notifications=notifications,
		log_level=log_level,
		log_file=log_file,
		log_format=log_format
	)


settings = load_settings()
