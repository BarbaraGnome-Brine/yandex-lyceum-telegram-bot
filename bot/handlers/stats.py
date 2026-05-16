import logging
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database import get_db_connection
from bot.locales import SUPPORTED_LANGUAGES, get_text
from bot.locales.translations import detect_language

logger = logging.getLogger(__name__)


# get_user_stats
def get_user_stats(user_id: int) -> dict:
    stats = {
        "total_messages": 0,
        "commands_used": 0,
        "anomalies_caused": 0,
        "last_active": None,
    }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM updates WHERE user_id = ?", (user_id,)
        )
        stats["total_messages"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM updates WHERE user_id = ? AND is_command = 1",
            (user_id,),
        )
        stats["commands_used"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM anomalies WHERE user_id = ?", (user_id,)
        )
        stats["anomalies_caused"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT MAX(timestamp) FROM updates WHERE user_id = ?", (user_id,)
        )
        row = cursor.fetchone()
        if row and row[0]:
            stats["last_active"] = row[0]

        conn.close()

    except Exception as e:
        logger.error(
            f"Failed to fetch stats for user {user_id}: {e}", exc_info=True
        )

    return stats


# stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    lang = context.user_data.get("language") or detect_language(update)

    user_stats = get_user_stats(user.id)

    header = get_text(
        "stats_personal_header", lang, username=user.username or user.first_name
    )
    parts = [header]

    parts.append(
        get_text("stats_messages", lang, count=user_stats["total_messages"])
    )
    parts.append(
        get_text(
            "stats_commands_used", lang, count=user_stats["commands_used"]
        )
    )
    parts.append(
        get_text(
            "stats_anomalies_caused",
            lang,
            count=user_stats["anomalies_caused"],
        )
    )

    last_active = user_stats["last_active"]
    if last_active:
        parts.append(get_text("stats_last_active", lang, datetime=last_active))
    else:
        parts.append(get_text("stats_no_activity", lang))

    message = "\n".join(parts)

    await context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode="HTML"
    )

    logger.info(f"User {user.id} requested /stats. Language: {lang}")


# get_handler
def get_handler():
    return CommandHandler("stats", stats)