from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.database import get_user_language
from bot.locales.translations import detect_language, get_text


# help_command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = (
        context.user_data.get('language')
        or get_user_language(update.effective_user.id)
        or detect_language(update)
    )

    help_text = {
        'ru': (
            "🗞 <b>Навигация по боту:</b>\n\n"
            "• /start - перезапуск\n"
            "• /stats - статистика\n"
            "• /settings - настройки\n"
            "• /language - сменить язык"
        ),
        'en': (
            "🗞 <b>Bot Navigation:</b>\n\n"
            "• /start - restart\n"
            "• /stats - statistics\n"
            "• /settings - settings\n"
            "• /language - change language"
        ),
        'sv': (
            "🗞 <b>Botnavigering:</b>\n\n"
            "• /start - omstart\n"
            "• /stats - statistik\n"
            "• /settings - inställningar\n"
            "• /language - ändra språk"
        )
    }

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text.get(lang, help_text['ru']),
        parse_mode="HTML"
    )


# get_handler
def get_handler():
    return CommandHandler('help', help_command)