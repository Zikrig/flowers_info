from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать отчет")]
        ],
        resize_keyboard=True
    )

def get_branches_keyboard(branches):
    keyboard = []
    for branch in branches:
        keyboard.append([InlineKeyboardButton(text=branch, callback_data=f"select_branch:{branch}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Управление филиалами", callback_data="manage_branches")],
        ]
    )

def get_branches_edit_keyboard(branches):
    keyboard = []
    for branch in branches:
        keyboard.append([InlineKeyboardButton(text=f"❌ {branch}", callback_data=f"del_branch:{branch}")])
    keyboard.append([InlineKeyboardButton(text="➕ Добавить филиал", callback_data="add_branch")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

