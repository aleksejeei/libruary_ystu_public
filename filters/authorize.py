from typing import Union
from typing import Union, Dict, Any
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import types
import db.control as db


auth = dict() # временное хранение значения принятия соглашения

class AuthFilter(Filter): # фильтр для сообщений

    """
    Фильтр для проверки принятия пользовательского соглашения.
    Пропускает только пользователей, НЕ давших согласие.
    """
    async def __call__(self, message: types.Message, **data: Dict[str, Any]) -> bool:
        user_id = message.from_user.id
        if user_id in auth:
            return auth[user_id]
        else:
            info = await db.readUserInfo(user_id)
            auth[user_id] = (info[0] == None or info[1] == None)

            return auth[user_id]


class AuthFilterCallback(Filter): # фильтр для callback
    """
       Фильтр для проверки принятия пользовательского соглашения.
       Возвращает True для пользователей, НЕ давших согласие (чтобы сработал обработчик).
       """

    async def __call__(self, callback: types.CallbackQuery, **data: Dict[str, Any]) -> bool:
        user_id = callback.from_user.id
        if user_id in auth:
            return auth[user_id]
        else:
            info = await db.readUserInfo(user_id)
            auth[user_id] = (info[0] == None or info[1] == None)
            return auth[user_id]