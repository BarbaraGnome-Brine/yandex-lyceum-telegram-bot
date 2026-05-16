from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.config import settings
from bot.locales.translations import get_text, detect_language


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
    Displays current bot configuration settings using the user's detected language.
    """
	lang = detect_language(update, context)

	# Map boolean settings to localized status strings
	alerts_status = get_text('enabled' if settings.notifications.alerts_enabled else 'disabled', lang)
	digest_status = get_text('enabled' if settings.notifications.digest_enabled else 'disabled', lang)

	# Format the message sections
	header = get_text('settings_header', lang)

	monitoring_info = get_text(
		'settings_monitoring',
		lang,
		interval=settings.monitoring.collection_interval,
		threshold=settings.monitoring.anomaly_threshold,
		retention=settings.monitoring.metrics_retention_days
	)

	notifications_info = get_text(
		'settings_notifications',
		lang,
		alerts=alerts_status,
		digest=digest_status,
		time=settings.notifications.digest_time
	)

	# Assemble and send
	full_message = f"{header}{monitoring_info}{notifications_info}"

	await update.effective_message.reply_text(
		text=full_message,
		parse_mode="HTML"
	)


def get_handler():
	return CommandHandler('settings', settings_handler)