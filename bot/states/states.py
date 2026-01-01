from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_for_phone = State()

class ReportState(StatesGroup):
    waiting_for_branch = State()
    waiting_for_kassa = State()

class AdminState(StatesGroup):
    waiting_for_branch_name = State()
    waiting_for_destination = State()

