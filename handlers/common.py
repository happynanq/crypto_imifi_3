from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
router = Router()
class UserState(StatesGroup):
    user_reg = State()
    admin_reg = State()
    user_fio = State()

# @router.message(Command(commands=["/menu"]))
# async def cmd_menu(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         text="Привет, зарегайся"
#              " /register",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await state.set_state(UserState.user_fio)

@router.message(StateFilter(None), Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Привет, чтобы начать квест введите ФИО и институт в одной строке "
             "",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.user_fio)



# Нетрудно догадаться, что следующие два хэндлера можно
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
# @router.message(StateFilter(None), Command(commands=["cancel"]))
# @router.message(default_state, F.text.lower() == "отмена")
# async def cmd_cancel_no_state(message: Message, state: FSMContext):
#     # Стейт сбрасывать не нужно, удалим только данные
#     await state.set_data({})
#     await message.answer(
#         text="Нечего отменять",
#         reply_markup=ReplyKeyboardRemove()
#     )
#
#
# @router.message(Command(commands=["cancel"]))
# @router.message(F.text.lower() == "отмена")
# async def cmd_cancel(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         text="Действие отменено",
#         reply_markup=ReplyKeyboardRemove()
#     )