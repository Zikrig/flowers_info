import asyncio
import time
import logging
from collections import deque
from aiogram import Bot
from bot.config import ADMIN_IDS, DELETE_AFTER_MINUTES, CHECK_INTERVAL, SETTINGS_FILE, GROUP_ID
from bot.utils.storage import read_json

logger = logging.getLogger(__name__)

# Dictionary to store message history in memory
message_history = {}
scanned_chats = set()

async def log_message(chat_id: int, message_id: int, user_id: int, timestamp: float = None):
    # Не логируем сообщения, отправленные в общую группу, чтобы их вообще не было в очереди на удаление
    if chat_id == GROUP_ID:
        return

    if chat_id not in message_history:
        message_history[chat_id] = deque(maxlen=100)
    
    if timestamp is None:
        timestamp = time.time()
        
    # Check if this message is already logged (to avoid duplicates from scan and normal flow)
    for entry in message_history[chat_id]:
        if entry["message_id"] == message_id:
            return

    message_history[chat_id].append({
        "message_id": message_id,
        "user_id": user_id,
        "timestamp": timestamp
    })
    logger.info(f"Logged message {message_id} in chat {chat_id} from user {user_id}")

async def scan_history(bot: Bot, chat_id: int, last_msg_id: int):
    if chat_id in scanned_chats:
        return
    
    # Don't scan the report group itself
    if chat_id == GROUP_ID:
        return

    logger.info(f"Scanning history for chat {chat_id}...")
    
    for i in range(1, 31):
        target_id = last_msg_id - i
        if target_id <= 0: break
        
        try:
            # Try to forward to get the date. Use GROUP_ID as a temporary buffer.
            tmp_msg = await bot.forward_message(chat_id=GROUP_ID, from_chat_id=chat_id, message_id=target_id)
            msg_date = tmp_msg.date.timestamp()
            msg_text = tmp_msg.text or tmp_msg.caption or ""
            await bot.delete_message(chat_id=GROUP_ID, message_id=tmp_msg.message_id)
            
            # Don't log /start command from history
            if msg_text == "/start":
                continue

            # Log it as a generic user message (user_id=0)
            await log_message(chat_id, target_id, 0, msg_date)
        except Exception:
            continue
            
    scanned_chats.add(chat_id)

async def auto_delete_task(bot: Bot):
    logger.info("Auto-delete task started")
    bot_id = int(bot.token.split(':')[0])
    
    while True:
        try:
            settings = await read_json(SETTINGS_FILE, {"auto_delete_admins": False})
            auto_delete_admins = settings.get("auto_delete_admins", False)
            
            now = time.time()
            
            for chat_id, messages in list(message_history.items()):
                # Не удаляем сообщения из общей группы отчетов
                if chat_id == GROUP_ID:
                    continue
                    
                to_delete_from_history = []
                
                for entry in list(messages):
                    age_minutes = (now - entry["timestamp"]) / 60
                    
                    if age_minutes >= DELETE_AFTER_MINUTES:
                        is_bot_msg = entry["user_id"] == bot_id
                        is_admin = entry["user_id"] in ADMIN_IDS
                        
                        should_delete = False
                        if is_bot_msg:
                            should_delete = True
                        elif is_admin:
                            if auto_delete_admins:
                                should_delete = True
                        else:
                            should_delete = True

                        if should_delete:
                            try:
                                await bot.delete_message(chat_id, entry["message_id"])
                                logger.info(f"Deleted message {entry['message_id']} in chat {chat_id}")
                            except Exception as e:
                                logger.debug(f"Could not delete {entry['message_id']}: {e}")
                            to_delete_from_history.append(entry)
                        else:
                            # If not deleted (admin), clean from history after 24h
                            if age_minutes > 1440:
                                to_delete_from_history.append(entry)
                
                for entry in to_delete_from_history:
                    try:
                        messages.remove(entry)
                    except ValueError:
                        pass
                        
        except Exception as e:
            logger.error(f"Error in auto_delete_task: {e}")
            
        await asyncio.sleep(CHECK_INTERVAL * 60)
