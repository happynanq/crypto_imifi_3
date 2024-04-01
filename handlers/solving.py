from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton, Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from keyboards.simple_row import make_row_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from datetime import datetime
from handlers.register import next_reg
from aiogram.utils.media_group import MediaGroupBuilder
from handlers.new_task import update_task
from aiogram.methods.send_media_group import SendMediaGroup
import json
from aiogram.types.input_file import InputFile
from PIL import Image
from helper.parse_json import update, get
from helper.get_bot import get_bot

# from register import next_reg # menu
class MyCallback(CallbackData, prefix = "mycb"):
    day: int
    foo : str

task_today = {
    1:[1],
    2:[2, 3],
    3: [4, 5],
    4: [6, 7],
    5: [8]
}
ways = ["Информация", "Посмотреть на доступные двери"]

router = Router()
class UserState(StatesGroup):
    user_reg = State()
class UserSolving(StatesGroup):
    user_solving = State()
class UserState(StatesGroup):
    user_reg = State()

@router.message(UserState.user_reg, F.text.lower() == "информация")
async def info_handl(message:Message, state:FSMContext):
    user = await state.get_data()
    print("USER: ", user)

    text = (user["user"]["fio_inst"]+ "\n"
            "Вы решили " + str(len(user["user"]["solved_task"])) + " задач"+"\n"
            )
    for i in range(len(user["user"]["solved_task"])):
        text += "[" + str(user["user"]["solved_task"][i]) + "]" + " - "
        text += user["user"]["solving_time"][i] +"\n"

    await message.answer(
        text=text

    )

@router.message(UserState.user_reg, F.text.lower() == "посмотреть на доступные двери")
async def task_dayly(message: Message, state: FSMContext):
    bot = get_bot()
    # await message.answer(
    #     text = "Смотрим",
    #     reply_markup=ReplyKeyboardRemove()
    # )
    user_data = await state.get_data()
    print("DATA: ", user_data["user"])
    # return
    user_datetime = user_data["user"]["date"]
    arr = []
    if user_datetime != 31:

        for k in range(1, min(6, user_datetime + 1)):
            for i in task_today[k]: #бляя даун рэндж полуинтервал
                if(i not in user_data["user"]["solved_task"]):
                    arr.append([InlineKeyboardButton(
                        text="Дверь #" + str(i),#oke
                        callback_data=MyCallback(day=i, foo="days").pack()
                    )])
        builder = InlineKeyboardMarkup(inline_keyboard = arr)

        await message.answer(
            text="Смотрим",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            "У вас есть доступ к этим дверям. \n (Если дверей нет, то дождитесь следующего сообщения.)",
            reply_markup=builder
        )
    else:
        await message.answer(
            text="Квест ещё не начался!"
        )
''' погоди а че вообще что то я улетел 
10-6; да я понимаю да я понимаю 
11-9; 
1-4;
3-5;
2-7;
'''
task_data = {
    1 : {
         "text"   : "На двери в первую комнату был нарисован глаз, который был перечеркнут. Зайдя в неё, ты увидел немного необычный стол и кубики на нём.",
         "text_ans":"Что там было написано?",
         "answer" : ["собака-поводырь", "собака поводырь"],
         "load_photo": "https://ibb.co/51R1Bj4",
         "load_video": ""
         },

    2 : {
         "text"   : "Комната за этой дверью была совершенно пуста. Единственным предметом здесь были висящие на стене необычные часы, которые когда-то давно остановились в одном положении. А ещё здесь был приятный аромат.",
          "text_ans":"Чем пахло в этой комнате?",
         "answer" : ["пиретрум", "пиретрумом"],
         "load_photo": "https://ibb.co/rQnTDq1",
         "load_video": ""
         },
     3: {"text"   : "За следующей дверью тебя ждала комната, в которой стоял старый телевизор, на котором транслировалась партия в шахматы. Как вдруг, не дойдя до финала, всё изменилась и теперь телевизор показывал лишь одну картинку.",
         "text_ans":"Что там было написано?",
         "answer" : ["СФУ","Сибирский федеральный Университет"],
         "load_photo": "https://ibb.co/L6GvPcX",
         "load_video": ""

     },
     # 5: {"text"   : "Ты подошел к первой двери. Она легко открылась, продемонстрировав тебе комнату, по центру в которой стояло радио. Едва переступив порог комнаты, ты услышал, что радио включилось.",
     #     "text_ans":"В каком году мир узнал о великом водиле?",
     #     "answer" : ["2011"],
     #     "load_photo": "/////////тут ссылка на аудиофайл" ,
     #     "load_video": ""
     #
     # },
     4 : {
         "text"   : "Вторая комната тебе показалась довольно уютной. Это была спальня с ничем не примечательной кроватью и ковром на стене. Вот он то и завладел твоим вниманием. Уж больно интересный он был. ",
         "text_ans":"Интересно, кто его создатели?",
         "answer" : ["Гастона Жюлиа и Пьера Фату","Гастон Жюлиа Пьер Фату","Жюлиа и Фату"],
         "load_photo": "https://ibb.co/SyNDN8c",
         "load_video": ""
         },
     5: {"text"   : "Эта дверь отличалась от всех предыдущих. Это была дверь сёдзи, традиционная японская дверь из полупрозрачной бумаги. Отодвинув её, оказался в комнате, а по центру увидел незаконченную партию игры в го. ",
         "text_ans":"Что хотели тебе показать люди, игравшие в го?",
         "answer" : ["Сакура", "Сакуру","Sakura"],
         "load_photo": "https://ibb.co/ph2j6wq",
         "load_video": ""

     },
     6: {"text"   : "За дверью находилась комната, напоминающая учебный класс. На столе лежала старая фотография этого же помещения, за столом сидел задумчивый мужчина.",
         "text_ans":"О чем думал этот мужчина?",
         "answer" : ["ИМиФИ"],
         "load_photo": "https://ibb.co/mFRb6GY",
         "load_video": ""

     },
     7: {
          "text": "За очередной дверью ты нашёл книжку с текстом и картинкой в ней. <Капитан Гронсвилд плыл на встречу с капитаном Ёжиком. Путь его лежал через туман, но он знал, что его друг находится где-то там. Чтобы не потеряться, он открыл карту>",
          "text_ans": "Где?",
          "answer": ["В тумане"],
          "load_photo": "https://ibb.co/nRT7tfK",
          "load_video": ""

          },
     8: {
          "text": "За этой дверью находился довольно уютный кабинет в английском стиле. Было видно, что хозяин кабинета не часто проводил здесь уборку. Осмотрев стол, ты заметил, что одна бумажка всё же выделяется на фоне остальных, но прочитав его несколько раз, так и не понял, что это.",
          "text_ans": " Ты видишь текст:\n" 
                      " Гафукупуек: уп ун о моц псоп оннушк фед аобс аматакп еф Л алобпуы ека аматакп еф Ы. Псун евжжабп нсеимг ва еид окнцад. Омм цедгг оспад екмы инаг цед саппад гдайиакбз ег псун пачнп гееч муча ук Акшгмунс мокшиоши. Псоп унк'п родп е ок окнцад. Уп огне б-бекпоукн о меп тунпоба ук редрена. Сососос уг ун заду фикс пв бдаопа теса окг теда тунпобаы. Ж.З.\n"
                      "О чем думал владелец в кабинете?",


          "answer": ["Функция","Функцию","Функции","Function"],
          "load_photo": "https://ibb.co/YhLbdpK",
          "load_video": ""
        }
}
# через кнопку
@router.callback_query(MyCallback.filter(F.foo == "days"))
async def send_task(callback: CallbackQuery, state : FSMContext, callback_data: MyCallback):
    # await update_task(callback, state)
    await callback.message.answer(
        text="Вы открыли дверь №" + str(callback_data.day),
        reply_markup=make_row_keyboard(["Назад"])
    )
    # for i in task_data[callback_data.day]:
    #     print(i)
    #ПОФИКСИТЬ НА task_today[callback_data.day]-----------------
    today_quest = task_data[callback_data.day]

    text_quest = today_quest["text"]

    await callback.message.answer(text=text_quest)
    # НЕ БУДЕТ РАБОТАТЬ

    if today_quest["load_photo"] != "":
        media_group = MediaGroupBuilder(
            # caption="й"
        )

        media_group.add_photo(
            media=today_quest["load_photo"]
            # media = "https://ibb.co/SyNDN8c"
        )
        await callback.message.answer_media_group(
            # media=album_builder.build()
            media = media_group.build()
        )
    await callback.message.answer(text=today_quest["text_ans"])

    user_data = await state.get_data()
    x = {"task_n": callback_data.day}
    user_data["user"].update(x)

    await state.update_data(user_data)
    await state.set_state(UserSolving.user_solving)
    await callback.answer()

@router.callback_query(MyCallback.filter(F.foo == "days"), Command("new_task")) # da  придумал вроде
async def send_task(callback: CallbackQuery, state : FSMContext, message: Message):
    await update_task(message, state)
    await callback.message.answer(text = "Куда пойдём?", reply_markup = make_row_keyboard(ways))
    await callback.answer()

# Тут проверять ответ
@router.message(UserSolving.user_solving, Command("cancel"))
async def solving_cancel(message:Message,  state : FSMContext):
    user_data = await state.get_data()
    del user_data["user"]["task_n"]
    print("HUETA ", user_data)
    await state.set_state(UserState.user_reg)
    await next_reg(message)


@router.message(UserSolving.user_solving)
async def solving(message:Message,  state : FSMContext):
    user_data = await state.get_data()
    print("1 - CALLBACCK USER DATA: ", user_data, "qwe", user_data["user"]["task_n"], type(user_data["user"]))
    print("PIPISKI: ", task_data[user_data["user"]["task_n"]]["answer"])
    ans = task_data[user_data["user"]["task_n"]]["answer"]
    ans_n = []
    for i in ans:
        ans_n.append(i.lower())
    if(message.text.lower() == "назад"):
        await solving_cancel(message, state)
    elif(message.text.lower() in ans_n):


        await message.reply(
            "Поздравляю! Это правильный ответ.",
        )

        #user_data["user"]
        print("Task_n: ", user_data["user"]["task_n"])
        # new_u_data = {user_data["user"]["solving_time"]
        user_data["user"]["solving_time"].append(str(datetime.now()))
        user_data["user"]["solved_task"].append(user_data["user"]["task_n"])
        del user_data["user"]["task_n"]
        await state.set_state(UserState.user_reg)
        user_data = await state.get_data()
        print(user_data)
        await next_reg(message)
        update(user_data["user"], "result.json")
    else:
        await message.reply(
            text="Неверный ответ! Попробуйте снова"
        )

