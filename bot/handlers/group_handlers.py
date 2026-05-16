import logging
import re
from datetime import datetime, timedelta

from telegram import ChatPermissions, Update
from telegram.ext import CommandHandler, ContextTypes, filters

from bot.database import add_warning, get_user_language, reset_warnings
from bot.locales.translations import detect_language, get_text

logger = logging.getLogger(__name__)

TIME_FORMAT = "%Y-%m-%d %H:%M"


# parse_duration
def parse_duration(duration_str: str) -> timedelta:
	units = {'d': 'days', 'h': 'hours', 'm': 'minutes'}
	match = re.match(r"(\d+)([dhm]?)", duration_str.lower())
	if not match:
		return timedelta(minutes=30)
	amount, unit = match.groups()
	return timedelta(**{units.get(unit, 'minutes'): int(amount)})


# get_mention
def get_mention(user):
	return f'<a href="tg://user?id={user.id}">{user.full_name}</a>'


# get_target_user
async def get_target_user(update: Update):
	if update.message.reply_to_message:
		return update.message.reply_to_message.from_user
	return None


# ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
	target = await get_target_user(update)
	lang = (
			context.user_data.get('language')
			or get_user_language(update.effective_user.id)
			or detect_language(update)
	)

	if not target:
		await update.message.reply_text(get_text('mod_usage_ban', lang))
		return

	period_str = context.args[0] if len(context.args) > 0 else "365d"
	reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason"

	now = datetime.now()
	until = now + parse_duration(period_str)

	try:
		await update.effective_chat.ban_member(target.id, until_date=until)
		reset_warnings(target.id, update.effective_chat.id)

		await update.message.reply_text(
			get_text(
				'mod_ban_success',
				lang,
				name=get_mention(target),
				moderator=get_mention(update.effective_user),
				time=now.strftime(TIME_FORMAT),
				until=until.strftime(TIME_FORMAT),
				reason=reason
			),
			parse_mode="HTML"
		)
	except Exception as e:
		await update.message.reply_text(f"Error: {e}")


# mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
	target = await get_target_user(update)
	lang = (
			context.user_data.get('language')
			or get_user_language(update.effective_user.id)
			or detect_language(update)
	)

	if not target:
		await update.message.reply_text(get_text('mod_usage_mute', lang))
		return

	period_str = context.args[0] if len(context.args) > 0 else "1h"
	reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason"

	now = datetime.now()
	until = now + parse_duration(period_str)

	try:
		await update.effective_chat.restrict_member(
			target.id,
			ChatPermissions(can_send_messages=False),
			until_date=until
		)
		await update.message.reply_text(
			get_text(
				'mod_mute_success',
				lang,
				name=get_mention(target),
				moderator=get_mention(update.effective_user),
				time=now.strftime(TIME_FORMAT),
				until=until.strftime(TIME_FORMAT),
				reason=reason
			),
			parse_mode="HTML"
		)
	except Exception as e:
		await update.message.reply_text(f"Error: {e}")


# warn
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
	target = await get_target_user(update)
	lang = (
			context.user_data.get('language')
			or get_user_language(update.effective_user.id)
			or detect_language(update)
	)

	if not target:
		await update.message.reply_text(get_text('mod_usage_warn', lang))
		return

	reason = " ".join(context.args) if context.args else "No reason"
	now = datetime.now()
	count = add_warning(target.id, update.effective_chat.id)

	if count >= 2:
		until = now + timedelta(days=7)
		try:
			await update.effective_chat.ban_member(target.id, until_date=until)
			reset_warnings(target.id, update.effective_chat.id)
			await update.message.reply_text(
				get_text(
					'mod_warn_ban',
					lang,
					name=get_mention(target),
					time=now.strftime(TIME_FORMAT),
					until=until.strftime(TIME_FORMAT)
				),
				parse_mode="HTML"
			)
		except Exception as e:
			await update.message.reply_text(f"Error during auto-ban: {e}")
	else:
		await update.message.reply_text(
			get_text(
				'mod_warn_success',
				lang,
				name=get_mention(target),
				count=count,
				moderator=get_mention(update.effective_user),
				time=now.strftime(TIME_FORMAT),
				reason=reason
			),
			parse_mode="HTML"
		)


# unban
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
	target = await get_target_user(update)
	lang = (
			context.user_data.get('language')
			or get_user_language(update.effective_user.id)
			or detect_language(update)
	)

	if not target:
		await update.message.reply_text(get_text('mod_usage_unban', lang))
		return

	try:
		await update.effective_chat.unban_member(target.id)
		await update.message.reply_text(
			get_text(
				'mod_unban_success',
				lang,
				name=get_mention(target),
				moderator=get_mention(update.effective_user)
			),
			parse_mode="HTML"
		)
	except Exception as e:
		await update.message.reply_text(f"Error: {e}")


# unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
	target = await get_target_user(update)
	lang = (
			context.user_data.get('language')
			or get_user_language(update.effective_user.id)
			or detect_language(update)
	)

	if not target:
		await update.message.reply_text(get_text('mod_usage_unmute', lang))
		return

	permissions = ChatPermissions(
		can_send_messages=True,
		can_send_polls=True,
		can_send_other_messages=True,
		can_add_web_page_previews=True
	)
	try:
		await update.effective_chat.restrict_member(
			target.id,
			permissions=permissions
		)
		await update.message.reply_text(
			get_text(
				'mod_unmute_success',
				lang,
				name=get_mention(target),
				moderator=get_mention(update.effective_user)
			),
			parse_mode="HTML"
		)
	except Exception as e:
		await update.message.reply_text(f"Error: {e}")


# get_handlers
def get_handlers():
	f = filters.ChatType.GROUPS | filters.ChatType.SUPERGROUP
	return [
		CommandHandler("ban", ban, filters=f),
		CommandHandler("mute", mute, filters=f),
		CommandHandler("warn", warn, filters=f),
		CommandHandler("unban", unban, filters=f),
		CommandHandler("unmute", unmute, filters=f)
	]