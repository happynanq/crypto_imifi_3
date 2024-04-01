from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from keyboards.simple_row import make_row_keyboard
import json
from helper.parse_json import get_all_chats
from helper.task_today import pp_task, ret_task
from helper.get_bot import get_bot
# from aiogram.utils.exceptions import BotBlocked
router = Router()
class UserState(StatesGroup):
    user_reg = State()
    admin_reg = State()

@router.message(UserState.admin_reg, F.text.lower() == "pip")
async def dice_day(message:Message, state:FSMContext):
    # await message.answer(text="Начался новый день задач!")
    chats, nicks = get_all_chats()
    bot = get_bot()
    pp_task()
    print("TASK: ", ret_task())
    i = 0
    for chat in chats:

        try:
            await bot.send_message(chat_id=chat, text="Начался новый день задач! /new_task")
        except Exception as E:
            await bot.send_message(chat_id=454676294, text = nicks[i])
            print("УЕБАН: ", chat)
            pass
        i += 1

@router.message(UserState.admin_reg, F.text.lower() == "res")
async def dice_day(message:Message, state:FSMContext):
    # await message.answer(text="Начался новый день задач!")
    chats, nicks = get_all_chats()
    bot = get_bot()
    i = 0
    for chat in chats:
        try:
            await bot.send_message(chat_id=chat, text="Ночью произошли изменеия с дверями, для продолжения нажмите: /start")
        except Exception as E:
            await bot.send_message(chat_id=454676294, text = nicks[i])

            print("УЕБАН: ", chat)
            pass
        i+=1

# че да