from aiogram import Router, types, F
import db.control as db
from parser.connect import AsyncApiClient
import keyboards as kb

router = Router()

@router.message(F.text) # поиск книг
async def simpleFindBooks(message: types.Message):
    info = await db.readUserInfo(message.from_user.id)
    name = info[0]
    id = info[1]
    obj = await AsyncApiClient.create(id, name)
    books = await obj.findBooks(message.text)
    if len(books) == 0:
        await message.answer('По вашему запросу ничего не найдено :(')
        await obj.closeSession()
        return
    id_book = books[0]['id']
    markDoc = books[0]['markDoc']
    marked = books[0]['isMarked']
    length = len(books)
    await obj.closeSession()
    await db.writeResult(message.chat.id, books)
    await message.answer(books[0]['book'], reply_markup=kb.startKb(id_book, markDoc, marked, length, current=0))

@router.callback_query(F.data.startswith("nextpage_")) # на следующую страницу
async def callbacks_num(callback: types.CallbackQuery):
    action = int(callback.data.split("_")[1])
    await callback.answer()
    books = await db.readResult(callback.from_user.id) # все книги
    if action > len(books)-1:
        action = 0
    elif action == -1:
        action = len(books)-1
    id_book = books[action]['id']
    markDoc = books[action]['markDoc']
    marked = books[action]['isMarked']
    length = len(books)
    await callback.message.edit_text(f'Страница {action+1}\n{books[action]['book']}', reply_markup=kb.startKb(id_book, markDoc, marked, length, current=action))

@router.callback_query(F.data.startswith("toorder-"))
async def callbacks_order(callback: types.CallbackQuery):
    book_id = callback.data.split("-")[1]
    current = callback.data.split("-")[2]
    source = callback.data.split("-")[3]
    info = await db.readUserInfo(callback.from_user.id)
    name = info[0]
    id = info[1]
    obj = await AsyncApiClient.create(id, name)
    funds = await obj.getFundLib(book_id)
    await obj.closeSession()
    text_add = '\n<b>Пункты книговыдачи</b>'
    for i in funds:
        text_add += f'\n{i['name']}:\nВсего - {i['total']}\nДоступно - {i['available']}\n'
    if source == 'search':
        keyboard = kb.funds(funds, current)
    elif source == 'listMarked':
        keyboard = kb.fundsMarkedList(funds, current)
    else:
        keyboard = kb.funds(funds, current)
    await callback.message.edit_text(callback.message.text+text_add, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()
    #print(funds)

@router.callback_query(F.data.startswith("finorder-"))
async def callbacks_finorder(callback: types.CallbackQuery):
    book_id = callback.data.split("-")[1]
    info = await db.readUserInfo(callback.from_user.id)
    name = info[0]
    id = info[1]
    obj = await AsyncApiClient.create(id, name)
    result = await obj.toOrderBook(book_id)
    await obj.closeSession()
    if result:
        await callback.message.edit_text("Книга отобрана для заказа", parse_mode="HTML", reply_markup=kb.finOrder())
    else:
        await callback.answer("Эта книга уже отобрана для заказа", show_alert=True)

