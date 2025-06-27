from aiogram import Bot
import logging
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

logger = logging.getLogger(__name__)


async def notify_telegram(text: str):
    try:
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=text)
    except Exception:
        logger.error("❗ Ошибка при отправке в Telegram:", exc_info=True)

