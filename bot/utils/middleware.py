import asyncio
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from bot.utils.deleter import log_message, scan_history

class DeletionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            # Don't log /start command
            if event.text == "/start":
                return await handler(event, data)

            # Log the user message with its actual date
            await log_message(event.chat.id, event.message_id, event.from_user.id, event.date.timestamp())
            
            # Start background history scan for this chat
            asyncio.create_task(scan_history(data['bot'], event.chat.id, event.message_id))
            
        return await handler(event, data)
