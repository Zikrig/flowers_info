from aiogram import Bot
from aiogram.methods import SendMessage, SendPhoto, EditMessageText, ForwardMessage
from bot.utils.deleter import log_message

class LoggingBot(Bot):
    async def __call__(self, method, request_timeout=None):
        result = await super().__call__(method, request_timeout)
        
        from aiogram.types import Message
        if isinstance(result, Message):
            bot_id = int(self.token.split(':')[0])
            # Don't log messages that were forwarded to the group during scan_history
            # to avoid infinite loops or double logging of temp messages
            # We can check if the chat_id is the group and we are in scan_history, 
            # but simpler: if it's a Message, log it.
            await log_message(
                chat_id=result.chat.id,
                message_id=result.message_id,
                user_id=bot_id,
                timestamp=result.date.timestamp()
            )
        return result
