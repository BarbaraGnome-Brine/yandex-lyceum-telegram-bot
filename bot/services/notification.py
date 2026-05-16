from telegram import Bot
from bot.config import settings
from bot.locales.translations import get_text
from bot.database import get_user_language, can_send_alert, update_alert_timestamp


async def send_anomaly_alert(bot: Bot, user_id: int, chat_id: int):
	cooldown = settings.notifications.alerts_cooldown_minutes  #
	if not can_send_alert(user_id, chat_id, cooldown):
		return

	try:
		chat = await bot.get_chat(chat_id)
		member = await bot.get_chat_member(chat_id, user_id)
		user = member.user

		full_name = f"{user.first_name} {user.last_name or ''}".strip()
		user_link = f'<a href="tg://user?id={user_id}">{full_name}</a>'
		chat_link = f'<a href="https://t.me/{chat.username}">{chat.title}</a>' if chat.username else f"<b>{chat.title}</b>"

		admins = await bot.get_chat_administrators(chat_id)
		update_alert_timestamp(user_id, chat_id)

		for admin in admins:
			if not admin.user.is_bot:
				lang = get_user_language(admin.user.id) or 'en'
				text = get_text('anomaly_alert', lang, user_link=user_link, chat_link=chat_link)

				try:
					await bot.send_message(chat_id=admin.user.id, text=text, parse_mode="HTML")
				except:
					continue

	except Exception as e:
		print(f"Alert failed: {e}")
