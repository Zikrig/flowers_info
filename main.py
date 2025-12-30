import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from bot.config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from bot.handlers import registration, employee, admin

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
dp.include_router(registration.router)
dp.include_router(admin.router)
dp.include_router(employee.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    logging.info(f"Webhook set to {WEBHOOK_URL}")
    yield
    # Shutdown
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Webhook removed")

# Create FastAPI application
app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Bot is running"}

