from telegram import Bot
from bot.config import settings
from bot.database import get_daily_chat_stats, get_user_language
from bot.locales.translations import get_text


async def send_daily_digest(bot: Bot):
	if not settings.notifications.digest_enabled:
		return

	stats = get_daily_chat_stats()

	for chat_id, data in stats.items():
		try:
			chat = await bot.get_chat(chat_id)
			chat_title = chat.title
			admins = await bot.get_chat_administrators(chat_id)

			for admin in admins:
				if admin.user.is_bot:
					continue
				lang = get_user_language(admin.user.id) or 'en'

				if data['messages'] == 0 and data['anomalies'] == 0:
					text = get_text('digest_empty', lang)
				else:
					header = get_text('digest_header', lang, chat_title=chat_title)
					body = get_text(
						'digest_body',
						lang,
						messages=data['messages'],
						users=data['users'],
						anomalies=data['anomalies']
					)
					text = f"{header}\n{body}"

				try:
					await bot.send_message(
						chat_id=admin.user.id,
						text=text,
						parse_mode="HTML"
					)
				except Exception:
					# Admin hasn't started a DM with the bot
					pass

		except Exception as e:
			print(f"Failed to send digest for chat {chat_id}: {e}")


async def get_digest_for_chat(bot: Bot, chat_id: int, admin_user_id: int):
	"""Generates and sends a digest for a specific chat to a specific admin."""
	stats = get_daily_chat_stats()

	# If there is no data for this chat yet
	if chat_id not in stats:
		lang = get_user_language(admin_user_id) or 'en'
		await bot.send_message(chat_id=admin_user_id, text=get_text('digest_empty', lang))
		return

	data = stats[chat_id]
	chat = await bot.get_chat(chat_id)
	lang = get_user_language(admin_user_id) or 'en'

	header = get_text('digest_header', lang, chat_title=chat.title)
	body = get_text(
		'digest_body',
		lang,
		messages=data['messages'],
		users=data['users'],
		anomalies=data['anomalies']
	)

	await bot.send_message(chat_id=admin_user_id, text=f"{header}\n{body}", parse_mode="HTML")
