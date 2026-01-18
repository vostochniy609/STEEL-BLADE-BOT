import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update, Message
from aiogram.enums import ParseMode

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # без /webhook
WEBHOOK_PATH = "/webhook"
WEBHOOK_FULL_URL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

COMMENT_TEXT = "Заранее подготовленный комментарий"

PORT = int(os.getenv("PORT", 8000))

# ================== ЛОГИ ==================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ================== BOT ==================

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ================== HANDLER ==================

@dp.channel_post()
async def on_channel_post(message: Message):
    logging.info("Новый пост в канале")

    linked_chat_id = message.chat.linked_chat_id

    logging.info(f"LINKED CHAT ID: {linked_chat_id}")
    logging.info(f"POST ID: {message.message_id}")

    if not linked_chat_id:
        logging.error("❌ У канала нет группы обсуждений")
        return

    try:
        await bot.send_message(
            chat_id=linked_chat_id,
            text=COMMENT_TEXT,
            reply_to_message_id=message.message_id
        )
        logging.info("✅ Комментарий отправлен")

    except Exception as e:
        logging.exception(f"❌ Ошибка отправки: {e}")

# ================== FASTAPI ==================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🔗 Установка webhook")
    await bot.set_webhook(WEBHOOK_FULL_URL)
    yield
    logging.info("🧹 Удаление webhook")
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "ok"}

# ================== START ==================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)




