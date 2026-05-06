import logging
from telegram.ext import ApplicationBuilder
from bot.config import BOT_TOKEN
from bot.handlers import start

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(start.get_handler())
    application.run_polling()