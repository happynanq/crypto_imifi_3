import asyncio
import logging
import sys
from datetime import datetime
from typing import Any, Callable, Dict, Awaitable

from aiogram import Bot, Dispatcher, Router, BaseMiddleware, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import admin, common, register, solving, new_task
from aiogram.types import FSInputFile
from helper.get_bot import bot_def, get_bot


async def main() -> None:
    bot_def()
    bot = get_bot()

    dp = Dispatcher()
    dp.include_router(admin.router)
    dp.include_router(new_task.router)
    dp.include_router(register.router)
    dp.include_router(solving.router)
    dp.include_router(common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    # ПОХУЙ