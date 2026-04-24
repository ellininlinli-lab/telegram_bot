import asyncio
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from rag import search, ask_llm

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "подписываемся на мой тгк и лайкаем все посты! https://t.me/dumblisa666"
        "Задай вопрос — и я отвечу по материалу."
    )

@dp.message()
async def handler(message: types.Message):
    q = message.text

    msg = await message.answer("🔍 ищу...")

    chunks = search(q)
    context = "\n\n".join(chunks)

    answer = ask_llm(context, q)

    await msg.edit_text(answer)

async def main():
    await dp.start_polling(bot)

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

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