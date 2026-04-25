import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# ====== ОБРАБОТКА СООБЩЕНИЙ ======
@dp.message()
async def handle_message(message: Message):
    await message.answer("Привет! Я работаю 🚀")

# ====== POLLING ======
async def main():
    print("Bot started")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# ====== HTTP сервер (для Render) ======
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

# ====== ЗАПУСК ======
if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    asyncio.run(main())