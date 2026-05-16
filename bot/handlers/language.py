import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from bot.database import set_user_language
from bot.locales import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)


# language_menu
async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Русский 🇷🇺", callback_data="set_lang_ru"),
        InlineKeyboardButton("Svenska 🇸🇪", callback_data="set_lang_sv"),
        InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Select Language / Выберите язык:"

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup
        )


# language_callback
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id

    if query.data == "open_lang_menu":
        await language_menu(update, context)
        return

    new_lang = query.data.replace("set_lang_", "")
    if new_lang in SUPPORTED_LANGUAGES:
        set_user_language(user_id, new_lang)
        context.user_data['language'] = new_lang

        msgs = {'ru': "✅ Готово!", 'en': "✅ Done!", 'sv': "✅ Klar!"}
        await query.answer(msgs.get(new_lang, msgs['en']))
        await query.edit_message_text(msgs.get(new_lang, msgs['en']))


# get_handlers
def get_handlers():
    return [
        CommandHandler('language', language_menu),
        CallbackQueryHandler(
            language_callback,
            pattern="^(set_lang_|open_lang_menu)"
        )
    ]