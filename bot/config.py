import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
# GROUP_ID и TOPIC_ID теперь задаются админом через интерфейс и сохраняются в settings.json
GROUP_ID = None
TOPIC_ID = None


DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BRANCHES_FILE = os.path.join(DATA_DIR, "branches.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

