from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database import get_db_connection
from bot.locales.translations import detect_language, get_text
from bot.services.digest_builder import get_digest_for_chat


# digest_command
async def digest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    lang = detect_language(update, context)

    if chat.type != "private":
        member = await chat.get_member(user.id)
        if member.status not in ['administrator', 'creator']:
            return

        try:
            await get_digest_for_chat(context.bot, chat.id, user.id)
            await update.message.reply_text(
                get_text('digest_sent_success', lang)
            )
        except Exception:
            await update.message.reply_text(
                get_text('digest_start_needed', lang)
            )
        return

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT chat_id FROM updates WHERE chat_id < 0")
    chats = c.fetchall()
    conn.close()

    found_any = False
    for row in chats:
        target_chat_id = row['chat_id']
        try:
            member = await context.bot.get_chat_member(
                target_chat_id,
                user.id
            )
            if member.status in ['administrator', 'creator']:
                await get_digest_for_chat(context.bot, target_chat_id, user.id)
                found_any = True
        except Exception:
            continue

    if not found_any:
        await update.message.reply_text(
            get_text('digest_no_admin_groups', lang)
        )


# get_handler
def get_handler():
    return CommandHandler("digest", digest_command)