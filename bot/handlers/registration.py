from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import USERS_FILE, ADMIN_IDS
from bot.states.states import Registration
from bot.keyboards.keyboards import get_phone_keyboard, get_main_keyboard
from bot.utils.storage import read_json, write_json

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    users = await read_json(USERS_FILE, {})
    user_id = str(message.from_user.id)
    
    if user_id in users:
        await message.answer(
            "Вы уже зарегистрированы! Отправьте любое сообщение или нажмите кнопку ниже, чтобы начать отчет.",
            reply_markup=get_main_keyboard()
        )
        return

    await state.set_state(Registration.waiting_for_phone)
    await message.answer(
        "Добро пожаловать! Для начала работы необходимо зарегистрироваться. "
        "Пожалуйста, отправьте свой номер телефона, нажав на кнопку ниже.",
        reply_markup=get_phone_keyboard()
    )

@router.message(Registration.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    users = await read_json(USERS_FILE, {})
    user_id = str(message.from_user.id)
    
    users[user_id] = {
        "phone": message.contact.phone_number,
        "full_name": message.from_user.full_name,
        "username": message.from_user.username
    }
    
    await write_json(USERS_FILE, users)
    await state.clear()
    
    await message.answer(
        f"Регистрация завершена! Ваш номер: {message.contact.phone_number}\n"
        "Теперь вы можете отправлять отчеты. Просто напишите любое сообщение или нажмите кнопку.",
        reply_markup=get_main_keyboard()
    )

