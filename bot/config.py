import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
GROUP_ID = int(os.getenv("GROUP_ID", 0))
TOPIC_ID = int(os.getenv("TOPIC_ID", 0))
DELETE_AFTER_MINUTES = int(os.getenv("DELETE_AFTER_MINUTES", 720))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BRANCHES_FILE = os.path.join(DATA_DIR, "branches.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

