import asyncio
import logging
import os
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.handlers import registration, employee, admin
from bot.utils.logging_bot import LoggingBot
from bot.utils.middleware import DeletionMiddleware
from bot.utils.deleter import auto_delete_task

async def main():
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    bot = LoggingBot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middlewares
    dp.message.middleware(DeletionMiddleware())

    # Handlers
    dp.include_router(registration.router)
    dp.include_router(admin.router)
    dp.include_router(employee.router)

    # Start auto-deletion task
    asyncio.create_task(auto_delete_task(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

