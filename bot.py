import asyncio
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@dp.message()
async def handler(message: types.Message):
    user_text = message.text

    msg = await message.answer("💭 думаю...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты полезный помощник."},
                {"role": "user", "content": user_text}
            ]
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Ошибка: {e}"

    await msg.edit_text(answer)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())