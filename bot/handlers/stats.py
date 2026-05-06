from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"👋 Привет, {update.effective_user.first_name}!\n"
             f"Я - <b>Brine Warrior</b>, твой личный помощник в управлении группами!", #TODO текст сообщения
        parse_mode="HTML"
    )

def get_handler():
    return CommandHandler('stats', stats)