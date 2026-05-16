import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, filters

from bot.database import get_user_language, set_user_language
from bot.locales import get_text
from bot.locales.translations import detect_language

logger = logging.getLogger(__name__)


# start_private
async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = (
        context.user_data.get("language")
        or get_user_language(user.id)
        or detect_language(update)
    )
    context.user_data["language"] = lang

    admin_rights = "restrict_members+delete_messages"
    group_url = f"https://t.me/{context.bot.username}?startgroup=true&admin={admin_rights}"

    keyboard = [
        [InlineKeyboardButton("➕ Add to Group / Добавить", url=group_url)],
        [
            InlineKeyboardButton(
                "🌐 Language / Язык", callback_data="open_lang_menu"
            )
        ],
    ]

    await update.message.reply_text(
        text=get_text("greeting", lang, first_name=user.first_name),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


# language_menu
async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Русский 🇷🇺", callback_data="set_lang_ru"),
        InlineKeyboardButton("Svenska 🇸🇪", callback_data="set_lang_sv"),
        InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en"),
    ]]
    text = "Select Language / Выберите язык:"
    if update.message:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard)
        )


# set_lang_callback
async def set_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    new_lang = query.data.replace("set_lang_", "")

    if query.data == "open_lang_menu":
        await language_menu(update, context)
        return

    set_user_language(user_id, new_lang)
    context.user_data["language"] = new_lang
    await query.answer("✅")
    await query.edit_message_text(f"Language: {new_lang}")


# get_handlers
def get_handlers():
    return [
        CommandHandler("start", start_private, filters=filters.ChatType.PRIVATE),
        CommandHandler(
            "language", language_menu, filters=filters.ChatType.PRIVATE
        ),
        CallbackQueryHandler(
            set_lang_callback, pattern="^(set_lang_|open_lang_menu)"
        ),
    ]