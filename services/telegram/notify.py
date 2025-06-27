from aiogram import Bot
import logging

logger = logging.getLogger(__name__)


async def notify_telegram(text: str):
    TELEGRAM_CHAT_ID = -4874157762
    try:
        async with Bot(token="7540596625:AAFmvy9fsfof5jaeiaLseFsmGfNgx6000_8") as bot:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception:
        logger.error("❗ Ошибка при отправке в Telegram:", exc_info=True)

