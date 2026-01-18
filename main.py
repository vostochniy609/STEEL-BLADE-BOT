import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

COMMENT_TEXT = "🔥 Обсуждаем пост в комментариях!"


@dp.channel_post()
async def on_channel_post(message: Message):
    # Проверяем, есть ли группа обсуждений
    if not message.chat.linked_chat_id:
        print("У канала нет привязанной группы обсуждений")
        return

    discussion_chat_id = message.chat.linked_chat_id

    try:
        await bot.send_message(
            chat_id=discussion_chat_id,
            text=COMMENT_TEXT,
            reply_to_message_id=message.message_id
        )
        print("Комментарий отправлен")
    except Exception as e:
        print("Ошибка отправки комментария:", e)


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Бот работает.")


# HTTP для Render
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


async def main():
    # отключаем webhook
    await bot.delete_webhook(drop_pending_updates=True)

    # HTTP для Render
    await start_http_server()

    # polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



