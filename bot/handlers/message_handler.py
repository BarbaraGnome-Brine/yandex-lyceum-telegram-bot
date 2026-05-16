import time
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from bot.database import get_db_connection

# handle_update
async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or update.effective_user.is_bot:
        return
    if not update.effective_chat:
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    msg = update.effective_message
    is_cmd = 1 if msg.text and msg.text.startswith('/') else 0


    current_time = time.time()

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO updates (timestamp, user_id, chat_id, is_command) "
        "VALUES (?, ?, ?, ?)",
        (current_time, user_id, chat_id, is_cmd)
    )
    conn.commit()
    conn.close()


    from bot.services.analyzer import check_for_anomalies
    from bot.services.notification import send_anomaly_alert

    if check_for_anomalies(user_id, chat_id):
        await send_anomaly_alert(context.bot, user_id, chat_id)


# get_handler
def get_handler():
    return MessageHandler(filters.ALL, handle_update)