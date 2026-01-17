import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTO_COMMENT_TEXT = "🗣 Обсуждаем пост в комментариях"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ---------- Telegram logic ----------

@dp.channel_post()
async def on_channel_post(message: Message):
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=AUTO_COMMENT_TEXT,
            reply_to_message_id=message.message_id
        )
    except Exception as e:
        print("Telegram error:", e)


# ---------- HTTP server (for Render) ----------

async def healthcheck(request):
    return web.Response(text="OK")


async def start_http_server():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"HTTP server started on port {port}")


# ---------- Main ----------

async def main():
    await start_http_server()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

