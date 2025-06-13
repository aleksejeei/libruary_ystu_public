from typing import Union, Dict, Any
from aiogram.filters import Filter
from aiogram import types
from aiogram.types import Message
import db.control as db

accepted = dict() # временное хранение значения принятия соглашения

class CheckAcceptFilter(Filter): # фильтр для сообщений

    """
    Фильтр для проверки принятия пользовательского соглашения.
    Пропускает только пользователей, НЕ давших согласие.
    """
    async def __call__(self, message: types.Message, **data: Dict[str, Any]) -> bool:
        user_id = message.from_user.id
        # print(accepted)
        if user_id in accepted: # если есть в ОЗУ
            # print('Сработало 1', not bool(accepted[user_id]))
            return not bool(accepted[user_id])
        else: # если нет в ОЗУ
            result = await db.acceptPrivacyRead(user_id)
            accepted[user_id] = result
            # print('Сработало 2', not bool(accepted[user_id]))
            return not bool(result)

class CheckAcceptFilterCallback(Filter): # фильтр для callback
    """
       Фильтр для проверки принятия пользовательского соглашения.
       Возвращает True для пользователей, НЕ давших согласие (чтобы сработал обработчик).
       """

    async def __call__(self, callback: types.CallbackQuery, **data: Dict[str, Any]) -> bool:
        user_id = callback.from_user.id

        # Проверяем кеш
        if user_id in accepted:
            return not accepted[user_id]  # True если нет согласия

        # Если нет в кеше - проверяем БД
        result = await db.acceptPrivacyRead(user_id)
        accepted[user_id] = result
        return not result  # True если нет согласия