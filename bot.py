import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

API_KEY = os.getenv("CEREBRAS_API_KEY")

@dp.message()
async def handler(message: types.Message):
    user_text = message.text

    msg = await message.answer("💭 думаю...")

    try:
        response = requests.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3.1-8b",
                "messages": [
                    {"role": "system", "content": "Ты полезный помощник."},
                    {"role": "user", "content": user_text}
                ],
                "temperature": 0.7
            }
        )

        answer = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        answer = f"Ошибка: {e}"

    await msg.edit_text(answer)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())