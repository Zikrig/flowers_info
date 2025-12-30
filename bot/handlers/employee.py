import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from bot.config import USERS_FILE, BRANCHES_FILE, GROUP_ID, TOPIC_ID
from bot.states.states import ReportState
from bot.keyboards.keyboards import get_branches_keyboard, get_main_keyboard
from bot.utils.storage import read_json

router = Router()

@router.callback_query(F.data.startswith("select_branch:"), ReportState.waiting_for_branch)
async def process_branch_callback(callback: CallbackQuery, state: FSMContext):
    branch = callback.data.split(":", 1)[1]
    
    await state.update_data(branch=branch, prompt_message_id=callback.message.message_id)
    await state.set_state(ReportState.waiting_for_kassa)
    
    # Edit the message to show selection and ask for kassa
    await callback.message.edit_text(
        f"Выбран филиал: {branch}\nТеперь отправьте фото или текст кассы:"
    )
    await callback.answer()

@router.message(F.chat.type == "private", StateFilter(None), F.text == "Создать отчет")
@router.message(F.chat.type == "private", StateFilter(None), ~F.text.startswith('/'))
@router.message(F.chat.type == "private", StateFilter(None), F.photo)
async def start_report(message: Message, state: FSMContext):
    users = await read_json(USERS_FILE, {})
    user_id = str(message.from_user.id)
    
    if user_id not in users:
        await message.answer("Сначала необходимо зарегистрироваться. Введите /start")
        return

    branches = await read_json(BRANCHES_FILE, [])
    if not branches:
        await message.answer("Список филиалов пуст. Обратитесь к администратору.")
        return

    await state.set_state(ReportState.waiting_for_branch)
    await state.update_data(start_message_id=message.message_id)
    await message.answer(
        "Выберите филиал, на котором вы находитесь:",
        reply_markup=get_branches_keyboard(branches)
    )

@router.message(F.chat.type == "private", ReportState.waiting_for_kassa)
async def process_kassa(message: Message, state: FSMContext):
    data = await state.get_data()
    branch = data.get("branch")
    prompt_message_id = data.get("prompt_message_id")
    start_message_id = data.get("start_message_id")
    
    users = await read_json(USERS_FILE, {})
    user_info = users.get(str(message.from_user.id), {})
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = f"{user_info.get('full_name', 'Неизвестно')}"
    username = f" (@{user_info.get('username')})" if user_info.get('username') else ""
    phone = user_info.get('phone', 'Неизвестно')
    
    caption = (
        f"📅 {now}\n"
        f"👤 {name}{username}\n"
        f"📞 {phone}\n"
        f"🏢 Филиал: {branch}\n"
        f"💰 Касса:\n"
    )

    if message.photo:
        photo = message.photo[-1].file_id
        text = message.caption if message.caption else ""
        caption += text
        await message.bot.send_photo(
            chat_id=GROUP_ID,
            message_thread_id=TOPIC_ID,
            photo=photo,
            caption=caption
        )
    else:
        caption += message.text if message.text else ""
        await message.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=caption
        )

    # Delete messages from private chat
    for msg_id in [start_message_id, prompt_message_id, message.message_id]:
        if msg_id:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
            except Exception:
                pass

    await state.clear()
    await message.answer("Ваш отчет получен, спасибо!", reply_markup=get_main_keyboard())

