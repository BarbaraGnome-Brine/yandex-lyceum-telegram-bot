import logging
from datetime import datetime
from telegram.ext import ApplicationBuilder
from bot.config import settings
from bot import database
from bot.services.digest_builder import send_daily_digest
from bot.handlers.digest import get_handler as get_digest_handler
from bot.handlers.start import get_handlers as get_start_handlers
from bot.handlers.group_handlers import get_handlers as get_group_handlers
from bot.handlers.stats import get_handler as get_stats_handler
from bot.handlers.help import get_handler as get_help_handler
from bot.handlers.settings_handler import get_handler as get_settings_handler
from bot.handlers.language import get_handlers as get_language_handlers

logging.basicConfig(format=settings.log_format, level=logging.INFO)
logger = logging.getLogger(__name__)


async def trigger_digest_job(context):
    await send_daily_digest(context.bot)


def register_handlers(application):
    for handler in get_start_handlers():
        application.add_handler(handler)
    for handler in get_language_handlers():
        application.add_handler(handler)

    application.add_handler(get_help_handler())
    application.add_handler(get_digest_handler())
    application.add_handler(get_settings_handler())

    for handler in get_group_handlers():
        application.add_handler(handler)

    application.add_handler(get_stats_handler())

    try:
        from bot.handlers.message_handler import get_handler as get_message_handler
        application.add_handler(get_message_handler())
    except:
        logger.warning("message_handler.py skipped.")

if __name__ == '__main__':
    database.init_db()
    application = ApplicationBuilder().token(settings.bot_token).build()
    if settings.notifications.digest_enabled:
        digest_time = datetime.time(hour=settings.notifications.digest_time, minute=0, second=0)
        application.job_queue.run_daily(
            trigger_digest_job,
            time=digest_time,
            name="daily_digest"
        )
        logger.info(f"Daily digest scheduled for {digest_time} server time.")

    register_handlers(application)
    print("Bot is running...")
    application.run_polling()