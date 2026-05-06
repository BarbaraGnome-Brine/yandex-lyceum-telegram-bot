# Initialize group_ids list if not exists
if 'group_ids' not in context.bot_data:
    context.bot_data['group_ids'] = set()

# When bot joins a new group, add it
def track_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member:
        chat = update.my_chat_member.chat
        if chat.type in ['group', 'supergroup']:
            if update.my_chat_member.new_chat_member.status in ['administrator', 'member']:
                context.bot_data.setdefault('group_ids', set()).add(chat.id)
            elif update.my_chat_member.new_chat_member.status == 'left':
                context.bot_data.get('group_ids', set()).discard(chat.id)