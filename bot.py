import asyncio
import os
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

from rag import search, ask_llm

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

MAX_LEN = 4000


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Привет! Задай вопрос по лекциям")


@dp.message()
async def handler(message: types.Message):
    q = message.text

    msg = await message.answer("💭 Думаю...")

    try:
        chunks = search(q)
        context = "\n\n".join(chunks)

        answer = await ask_llm(context, q)

        MAX_LEN = 4000
        if len(answer) > MAX_LEN:
            answer = answer[:MAX_LEN] + "\n\n✂️ Ответ обрезан"

    except Exception as e:
        answer = f"❌ Ошибка: {e}"

    await msg.edit_text(answer)

async def main():
    await dp.start_polling(bot)


# сервер для Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    asyncio.run(main())