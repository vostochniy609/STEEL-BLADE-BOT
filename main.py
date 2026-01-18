import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ====== ХЭНДЛЕР ЛИЧНЫХ СООБЩЕНИЙ ======
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот запущен и работает.")


# ====== ХЭНДЛЕР ПОСТОВ В КАНАЛЕ ======
@dp.channel_post()
async def on_channel_post(message: Message):
    print("NEW POST:", message.chat.id, message.message_id)


# ====== HTTP-СЕРВЕР ДЛЯ RENDER ======
async def start_http_server():
    app = web.Application()

    async def healthcheck(request):
        return web.Response(text="OK")

    app.router.add_get("/", healthcheck)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )
    await site.start()


# ====== MAIN ======
async def main():
    # КРИТИЧНО: удаляем webhook
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем HTTP-сервер (Render требует)
    await start_http_server()

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


