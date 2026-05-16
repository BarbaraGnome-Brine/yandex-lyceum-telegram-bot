from typing import Dict, Optional

SUPPORTED_LANGUAGES = ["ru", "en", "sv"]
DEFAULT_LANGUAGE = "en"

MESSAGES: Dict[str, Dict[str, str]] = {
    "greeting": {
        "ru": "👋 Привет, {first_name}!\n\nЯ — <b>Brine Warrior</b>, твой личный помощник по управлению группами!\n\nИспользуй /help для просмотра команд.",
        "en": "👋 Hello, {first_name}!\n\nI'm <b>Brine Warrior</b>, your personal group management assistant!\n\nUse /help to see the list of commands.",
        "sv": "👋 Hej, {first_name}!\n\nJag är <b>Brine Warrior</b>, din personliga assistent för grupphantering!\n\nAnvänd /help för att se kommandolistan.",
    },
    "select_language": {
        "ru": "🌐 Пожалуйста, выберите язык интерфейса:",
        "en": "🌐 Please select the interface language:",
        "sv": "🌐 Vänligen välj gränssnittsspråk:",
    },
    "lang_updated": {
        "ru": "✅ Язык успешно изменен!",
        "en": "✅ Language updated successfully!",
        "sv": "✅ Språket har изменился!",
    },
    "mod_ban_success": {
        "ru": "🔨 <b>Бан выдан пользователю:</b> {name}\n🛡️ <b>Модератор:</b> {moderator}\n📅 <b>Когда:</b> {time}\n⌛ <b>Окончание:</b> {until}\n📝 <b>Причина:</b> {reason}",
        "en": "🔨 <b>Ban issued to:</b> {name}\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>When:</b> {time}\n⌛ <b>Finish:</b> {until}\n📝 <b>Reason:</b> {reason}",
        "sv": "🔨 <b>Bannlysning utfärdad till:</b> {name}\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>När:</b> {time}\n⌛ <b>Slutar:</b> {until}\n📝 <b>Anledning:</b> {reason}",
    },
    "mod_mute_success": {
        "ru": "🔇 <b>Мут выдан пользователю:</b> {name}\n🛡️ <b>Модератор:</b> {moderator}\n📅 <b>Когда:</b> {time}\n⌛ <b>Окончание:</b> {until}\n📝 <b>Причина:</b> {reason}",
        "en": "🔇 <b>Mute issued to:</b> {name}\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>When:</b> {time}\n⌛ <b>Finish:</b> {until}\n📝 <b>Reason:</b> {reason}",
        "sv": "🔇 <b>Tystnad utfärdad till:</b> {name}\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>När:</b> {time}\n⌛ <b>Slutar:</b> {until}\n📝 <b>Anledning:</b> {reason}",
    },
    "mod_warn_success": {
        "ru": "⚠️ <b>Предупреждение выдано пользователю:</b> {name} ({count}/2)\n🛡️ <b>Модератор:</b> {moderator}\n📅 <b>Когда:</b> {time}\n📝 <b>Причина:</b> {reason}",
        "en": "⚠️ <b>Warning issued to:</b> {name} ({count}/2)\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>When:</b> {time}\n📝 <b>Reason:</b> {reason}",
        "sv": "⚠️ <b>Varning utfärdad till:</b> {name} ({count}/2)\n🛡️ <b>Moderator:</b> {moderator}\n📅 <b>När:</b> {time}\n📝 <b>Anledning:</b> {reason}",
    },
    "mod_warn_ban": {
        "ru": "🚫 <b>Автоматический бан:</b> {name}\n📝 <b>Причина:</b> Превышено число предупреждений (2/2)\n📅 <b>Когда:</b> {time}\n⌛ <b>Окончание:</b> {until}",
        "en": "🚫 <b>Automatic Ban:</b> {name}\n📝 <b>Reason:</b> Too many warnings (2/2)\n📅 <b>When:</b> {time}\n⌛ <b>Finish:</b> {until}",
        "sv": "🚫 <b>Automatiskt Ban:</b> {name}\n📝 <b>Anledning:</b> För många varningar (2/2)\n📅 <b>När:</b> {time}\n⌛ <b>Slutar:</b> {until}",
    },
    "mod_unban_success": {
        "ru": "✅ <b>Разбан:</b> Ограничения с пользователя {name} сняты.\n🛡️ <b>Модератор:</b> {moderator}",
        "en": "✅ <b>Unban:</b> Restrictions lifted for {name}.\n🛡️ <b>Moderator:</b> {moderator}",
        "sv": "✅ <b>Obannad:</b> Restriktioner borttagna för {name}.\n🛡️ <b>Moderator:</b> {moderator}",
    },
    "mod_unmute_success": {
        "ru": "🔊 <b>Анмут:</b> С пользователя {name} снят режим молчания.\n🛡️ <b>Модератор:</b> {moderator}",
        "en": "🔊 <b>Unmute:</b> Mute lifted for {name}.\n🛡️ <b>Moderator:</b> {moderator}",
        "sv": "🔊 <b>Avtystad:</b> Tystnad borttagen för {name}.\n🛡️ <b>Moderator:</b> {moderator}",
    },
    "mod_usage_ban": {
        "ru": "⚠️ Использование: ответьте на сообщение + <code>/ban 1d причина</code>",
        "en": "⚠️ Usage: reply to a message + <code>/ban 1d reason</code>",
        "sv": "⚠️ Användнение: svara på ett meddelande + <code>/ban 1d anledning</code>",
    },
    "mod_usage_mute": {
        "ru": "⚠️ Использование: ответьте на сообщение + <code>/mute 1h</code>",
        "en": "⚠️ Usage: reply to a message + <code>/mute 1h</code>",
        "sv": "⚠️ Användning: svara på ett meddelande + <code>/mute 1h</code>",
    },
    "mod_usage_unban": {
        "ru": "⚠️ Использование: ответьте на сообщение пользователя, которого нужно разбанить.",
        "en": "⚠️ Usage: reply to the message of the user you want to unban.",
        "sv": "⚠️ Användning: svara på meddelandet från användaren du vill obanna.",
    },
    "mod_usage_unmute": {
        "ru": "⚠️ Использование: ответьте на сообщение пользователя, чтобы снять мут.",
        "en": "⚠️ Usage: reply to the message of the user to unmute.",
        "sv": "⚠️ Användning: svara på meddelandet från användaren för att ta bort tystnaden.",
    },
    "mod_usage_warn": {
        "ru": "⚠️ Использование: ответьте на сообщение + /warn",
        "en": "⚠️ Usage: reply to a message + /warn",
        "sv": "⚠️ Användning: svara på ett meddelande + /warn",
    },
    "stats_personal_header": {
        "ru": "📊 <b>Статистика пользователя {username}:</b>",
        "en": "📊 <b>Personal Stats for {username}:</b>",
        "sv": "📊 <b>Personlig statistik för {username}:</b>",
    },
    "stats_messages": {
        "ru": "• Сообщений: {count}",
        "en": "• Messages: {count}",
        "sv": "• Meddelanden: {count}",
    },
    "stats_commands_used": {
        "ru": "• Использовано команд: {count}",
        "en": "• Commands used: {count}",
        "sv": "• Kommandon som används: {count}",
    },
    "stats_anomalies_caused": {
        "ru": "• Вызвано аномалий: {count}",
        "en": "• Anomalies you triggered: {count}",
        "sv": "• Avvikelser du orsakat: {count}",
    },
    "stats_last_active": {
        "ru": "• Последняя активность: {datetime}",
        "en": "• Last active: {datetime}",
        "sv": "• Senast aktiv: {datetime}",
    },
    "stats_no_activity": {
        "ru": "• Пока нет зарегистрированной активности",
        "en": "• No activity recorded yet",
        "sv": "• Ingen aktivitet registrerad än",
    },
    "settings_header": {
        "ru": "⚙️ <b>Настройки системы</b>",
        "en": "⚙️ <b>System Settings</b>",
        "sv": "⚙️ <b>Systeminställningar</b>",
    },
    "settings_monitoring": {
        "ru": "\n\n📊 <b>Мониторинг:</b>\n• Интервал сбора: {interval}с\n• Порог аномалий: {threshold}\n• Хранение метрик: {retention} дн.",
        "en": "\n\n📊 <b>Monitoring:</b>\n• Collection interval: {interval}s\n• Anomaly threshold: {threshold}\n• Metrics retention: {retention} days",
        "sv": "\n\n📊 <b>Övervakning:</b>\n• Insamlingsintervall: {interval}s\n• Tröskelvärde för anomali: {threshold}\n• Lagring av mätvärden: {retention} dagar",
    },
    "settings_notifications": {
        "ru": "\n\n🔔 <b>Уведомления:</b>\n• Алерты: {alerts}\n• Дайджест: {digest}\n• Время дайджеста: {time}:00",
        "en": "\n\n🔔 <b>Notifications:</b>\n• Alerts: {alerts}\n• Digest: {digest}\n• Digest time: {time}:00",
        "sv": "\n\n🔔 <b>Aviseringar:</b>\n• Varningar: {alerts}\n• Sammanfattning: {digest}\n• Tid för sammanfattning: {time}:00",
    },
    "enabled": {
        "ru": "✅ Включено",
        "en": "✅ Enabled",
        "sv": "✅ Aktiverad",
    },
    "disabled": {
        "ru": "❌ Выключено",
        "en": "❌ Disabled",
        "sv": "❌ Inaktiverad",
    },
    "anomaly_alert": {
        "ru": "⚠️ Обнаружен спам от {user_link} в группе {chat_link}!",
        "en": "⚠️ Spam detected from {user_link} in group {chat_link}!",
        "sv": "⚠️ Spam upptäckt från {user_link} i gruppen {chat_link}!",
    },
    "digest_header": {
        "ru": "📊 <b>Ежедневный дайджест для {chat_title}</b>\nЗа последние 24 часа:",
        "en": "📊 <b>Daily Digest for {chat_title}</b>\nOver the last 24 hours:",
        "sv": "📊 <b>Daglig sammanfattning för {chat_title}</b>\nUnder de senaste 24 timmarna:",
    },
    "digest_body": {
        "ru": "• Отправлено сообщений: <b>{messages}</b>\n• Активных пользователей: <b>{users}</b>\n• Обнаружено спам-аномалий: <b>{anomalies}</b>",
        "en": "• Messages sent: <b>{messages}</b>\n• Active users: <b>{users}</b>\n• Spam anomalies detected: <b>{anomalies}</b>",
        "sv": "• Skickade meddelanden: <b>{messages}</b>\n• Aktiva användare: <b>{users}</b>\n• Spam-anomalier upptäckta: <b>{anomalies}</b>",
    },
    "digest_empty": {
        "ru": "💤 За последние 24 часа активности не было.",
        "en": "💤 No activity recorded in the last 24 hours.",
        "sv": "💤 Ingen aktivitet registrerad under de senaste 24 timmarna.",
    },
    "digest_sent_success": {
        "ru": "✅ Статистика отправлена вам в ЛС!",
        "en": "✅ Statistics sent to your DMs!",
        "sv": "✅ Statistik har skickats till dina privata meddelanden!",
    },
    "digest_start_needed": {
        "ru": "❌ Пожалуйста, напишите мне в личку /start, чтобы я мог прислать отчет.",
        "en": "❌ Please start a private chat with me (/start) so I can send you the report.",
        "sv": "❌ Vänligen starta en chatt med mig (/start) så att jag kan skicka rapporten.",
    },
    "digest_no_admin_groups": {
        "ru": "🔍 Я не нашел групп, в которых вы являетесь администратором.",
        "en": "🔍 I couldn't find any groups where you are an administrator.",
        "sv": "🔍 Jag hittade inga grupper där du är administratör.",
    },
}


# get_text
def get_text(key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    message = MESSAGES.get(key, {}).get(language)

    if message is None:
        message = MESSAGES.get(key, {}).get(DEFAULT_LANGUAGE, key)

    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError:
            pass
    return message


# detect_language
def detect_language(update, context=None) -> str:
    if context is not None and "language" in context.user_data:
        return context.user_data["language"]
    user = update.effective_user
    if user and user.language_code:
        code = user.language_code.lower()[:2]
        if code in SUPPORTED_LANGUAGES:
            return code

    return DEFAULT_LANGUAGE