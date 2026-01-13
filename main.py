import asyncio
from aiogram import Bot, Dispatcher, types
import os

TOKEN = os.getenv("BOT_TOKEN")
DISCUSSION_CHAT_ID = int(os.getenv("DISCUSSION_CHAT_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.channel_post()
async def on_new_post(message: types.Message):
    rules_text = (
        "⚠️ НЕ НАРУШАЙ ПРАВИЛА!\n\n"
        "1. Реклама / пиар / нецензурный контент / слитые данные / треки / "
        "попрошайничество / политика — БАН\n"
        "2. Создание фейковых аккаунтов медийных личностей — БАН\n"
        "3. Администрация оставляет за собой право блокировки на своё усмотрение"
    )

    await bot.send_message(
        chat_id=DISCUSSION_CHAT_ID,
        text=rules_text
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
