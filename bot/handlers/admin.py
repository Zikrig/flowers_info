from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.config import ADMIN_IDS, BRANCHES_FILE
from bot.states.states import AdminState
from bot.keyboards.keyboards import (
    get_admin_keyboard, 
    get_branches_edit_keyboard
)
from bot.utils.storage import read_json, write_json

router = Router()

@router.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def cmd_admin(message: Message):
    await message.answer("Панель администратора:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "admin_main", F.from_user.id.in_(ADMIN_IDS))
async def back_to_admin(callback: CallbackQuery):
    await callback.message.edit_text("Панель администратора:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "manage_branches", F.from_user.id.in_(ADMIN_IDS))
async def manage_branches(callback: CallbackQuery):
    branches = await read_json(BRANCHES_FILE, [])
    await callback.message.edit_text(
        "Список филиалов (нажмите, чтобы удалить):", 
        reply_markup=get_branches_edit_keyboard(branches)
    )

@router.callback_query(F.data == "add_branch", F.from_user.id.in_(ADMIN_IDS))
async def add_branch_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.waiting_for_branch_name)
    await callback.message.edit_text("Введите название нового филиала:")

@router.message(AdminState.waiting_for_branch_name, F.from_user.id.in_(ADMIN_IDS))
async def add_branch_finish(message: Message, state: FSMContext):
    new_branch = message.text.strip()
    branches = await read_json(BRANCHES_FILE, [])
    if new_branch not in branches:
        branches.append(new_branch)
        await write_json(BRANCHES_FILE, branches)
        await message.answer(f"Филиал '{new_branch}' добавлен.")
    else:
        await message.answer(f"Филиал '{new_branch}' уже существует.")
    
    await state.clear()
    await cmd_admin(message)

@router.callback_query(F.data.startswith("del_branch:"), F.from_user.id.in_(ADMIN_IDS))
async def delete_branch(callback: CallbackQuery):
    branch_to_del = callback.data.split(":", 1)[1]
    branches = await read_json(BRANCHES_FILE, [])
    if branch_to_del in branches:
        branches.remove(branch_to_del)
        await write_json(BRANCHES_FILE, branches)
    
    await manage_branches(callback)


