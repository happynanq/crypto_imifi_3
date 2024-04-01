from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from keyboards.simple_row import make_row_keyboard
import json
from helper.parse_json import update, get, load_data
from helper.task_today import today_task
from handlers.new_task import update_task
router = Router()
moves = ["Осмотреться"]

class UserState(StatesGroup):
    user_reg = State()
    admin_reg = State()
    user_fio = State()


# тут зарегать, что у него все по нулям и предложить решать задачки
# так же зарегать текущую дату, когда все решает, будем предлагать на некст
# и изменять его дату


@router.message(UserState.user_fio)
async def cmd_reg(message: Message, state: FSMContext):
    f, s = load_data(message.from_user.id)
    # print("deanon: ", )

    print("FS: ", f, s)
    user_data = {"date": datetime.now().day, #! ПОПРОВИТЬ НА datetime.now().day
                 "fio_inst" : message.text,
                 "id":message.from_user.id,
                 "solving_time": f,
                 "solved_task":s,
                 "deanon": message.from_user.username
                 }
    print("My ID: ", message.from_user.id)
    #454676294
    update(user_data, "result.json")
    # with open('result.json', 'w') as fp:
    #     json.dump([user_data], fp)
    print(get(message.from_user.id, "result.json"))
    await state.update_data(user=user_data)
    # Устанавливаем пользователю состояние "зареганный"
    if(message.from_user.id == 454676294):
        print("Hello admin")
        await message.answer(
            text="Админка",
            reply_markup=make_row_keyboard(["ban", "pip"] )
        )
        await state.set_state(UserState.admin_reg)
    else:
        await message.answer(
            text="Ты очнулся в тёмном тихом коридоре. Оглянувшись, заметил, что в едва освещенном лампочкой пространстве не видно было ни одного окна, лишь две двери находятся перед тобой. Проверив все карманы на наличие какого-либо средства связи, понял, что у тебя с собой абсолютно ничего нет, как и воспоминаний о том, как ты попал в это помещение. ",
            reply_markup=make_row_keyboard(moves)
        )
        await update_task(message, state, 0)
        await state.set_state(UserState.user_reg)

@router.message( Command("register"))
async def cmd_reg_err(message: Message, state: FSMContext):
    await message.answer(
        text="Вы были уже зарегистрированы!",
        reply_markup=make_row_keyboard(moves)
    )
    # user_data = {"date": datetime.now().day}
    # await state.update_data(user=user_data)
    # # Устанавливаем пользователю состояние "зареганный"
    # await state.set_state(UserState.user_reg)


ways = ["Информация", "Посмотреть на доступные двери"]



@router.message(UserState.user_reg, F.text.lower() == "осмотреться")
async def next_reg(message:Message):
    await message.answer(
        text = "Куда пойдём?",
        reply_markup = make_row_keyboard(ways)
    )



