import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.handlers import registration, employee, admin

async def main():
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Handlers
    dp.include_router(registration.router)
    dp.include_router(admin.router)
    dp.include_router(employee.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

