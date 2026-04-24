import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

from rag import search, ask_llm

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


# ✅ /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "подпишитесь на мой тгк и лайкайте все посты https://t.me/dumblisa666"
        "Задай вопрос — и я отвечу по материалу."
    )


# ✅ основной обработчик
@dp.message()
async def handler(message: types.Message):
    q = message.text

    msg = await message.answer("🔎 Ищу...")

    try:
        # поиск по базе
        chunks = search(q)
        context = "\n\n".join(chunks)

        # ВАЖНО: await
        answer = await ask_llm(context, q)

        await msg.edit_text(answer)

    except Exception as e:
        await msg.edit_text(f"❌ Ошибка: {e}")


# запуск
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())