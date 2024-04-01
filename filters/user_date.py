from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

class UserDataFilter(BaseFilter):
    def __init__(self, date: Union[str]):
        self.date = date

    # async def __call__(self, message:Message):