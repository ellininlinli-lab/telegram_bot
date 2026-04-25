import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from rag import search, ask_llm

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

MAX_LEN = 4000


# ===== /start =====
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Привет! Задай вопрос по лекциям")


# ===== основной обработчик =====
@dp.message()
async def handler(message: types.Message):
    q = message.text

    msg = await message.answer("💭 Думаю...")

    try:
        # 🔍 поиск по базе
        chunks = search(q)
        context = "\n\n".join(chunks)

        # 🤖 запрос к ИИ
        answer = await ask_llm(context, q)

        # ✂️ ограничение Telegram
        if len(answer) > MAX_LEN:
            answer = answer[:MAX_LEN] + "\n\n✂️ Ответ обрезан"

    except Exception as e:
        print("ERROR:", e)
        answer = f"❌ Ошибка: {e}"

    await msg.edit_text(answer)


# ===== запуск бота =====
async def main():
    print("Bot started")

    # 🔥 убираем конфликт Telegram
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


# ===== сервер для Render =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}")
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# ===== запуск =====
if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    asyncio.run(main())