from parser.connect import AsyncApiClient
import db.control as db
import datetime
import asyncio
from aiogram import Bot

async def push(user_id):
    info = await db.readUserInfo(user_id)
    rdr_name = info[0]
    rdr_id = info[1]
    obj = await AsyncApiClient.create(rdr_id, rdr_name)
    books = await obj.receivedBooks()
    await obj.closeSession()
    ##print(books)
    now = datetime.datetime.now()
    #print(now)
    listen_days = list()
    for book in books:
        date_return = datetime.datetime.strptime(book['date_return'], '%d.%m.%Y')
        # print(date_return)
        count_days = ((date_return-now).days)
        listen_days.append(count_days)
    minDaysToReturn = min(listen_days)

    return [minDaysToReturn in [3, 2, 1, 7], minDaysToReturn]


async def mainPush(bot: Bot):
    usersIds = await db.readUsersId()
    for user_id in usersIds:
        try:
            result = await push(user_id)
        except:
            result = [False, False]
        if result[0]:
            try:
                await bot.send_message(chat_id=user_id, text=f'Через {result[1]} дней наступает срок сдачи одной или нескольких книг.')
            except Exception as e:
                print(f"Ошибка отправки для {user_id}: {e}")
            print('Скоро сдавать книги')
        await asyncio.sleep(0.1)