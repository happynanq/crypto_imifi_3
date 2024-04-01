from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from keyboards.simple_row import make_row_keyboard
import json
from helper.parse_json import update, get
from helper.task_today import ret_task

router = Router()
class UserState(StatesGroup):
    user_reg = State()
    admin_reg = State()

# начался новый день задач!
ways = ["Информация", "Посмотреть на доступные двери"]

@router.message(UserState.user_reg, Command("new_task"))
async def update_task(message: Message, state:FSMContext, q = 1):
    user_data = await state.get_data()
    print("USER_UPDATE ", user_data)
    user_data["user"]["date"] = ret_task()
    user_data = await state.get_data()
    print("USER_UPDATE2 ", user_data)
    if(user_data["user"]["date"] > 5 ):
        await message.answer("На расстоянии нескольких десятков метров от тебя стоял вертолет с эмблемой Цикады. Из него вышел человек в маске без лица и протянул тебе руку со словами: “Поздравляю, вы прошли игру”.")
        return
    if(q):
        await message.answer(
            text="Куда пойдём?",
            reply_markup=make_row_keyboard(ways)
        )
