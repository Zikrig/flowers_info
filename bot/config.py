import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
GROUP_ID = int(os.getenv("GROUP_ID", 0))
TOPIC_ID = int(os.getenv("TOPIC_ID", 0))

# Webhook settings
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BRANCHES_FILE = os.path.join(DATA_DIR, "branches.json")

