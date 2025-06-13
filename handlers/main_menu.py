from aiogram.filters.command import Command
from aiogram import F, types, Router
import accepts
import keyboards as kb
import db.control as db
from parser.connect import AsyncApiClient
from parser.check_auth import checkAuth
import filters.accept as acceptFilter
import filters.authorize as authorize
import push

router = Router()

markedBooksAllUsers = dict() # "ОЗУ" для отмеченных книг (для пагинации)
received_books = dict() # "ОЗУ" для полученных книг(для пагинации)
selectedBooks = dict()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    print('Ошибка тут 1')
    await message.answer("Для поиска просто напишите название книги в чат.\nПомощь по боту: /help", reply_markup=kb.menu())

@router.callback_query(F.data == "start")
async def callbacks_start(callback: types.CallbackQuery):
    await callback.message.edit_text("Для поиска просто напишите название книги в чат.\nПомощь по боту: /help",
                         reply_markup=kb.menu())

@router.callback_query(F.data.startswith("markDoc-"))
async def callbacks_markDoc(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    actions = {'del': False, 'add': True}
    action = callback.data.split("-")[1] # add или del
    markDoc = callback.data.split("-")[2] # id для отметки книги/документа
    currentPage = int(callback.data.split("-")[3]) # текущая страница для пагинации
    forWhat = callback.data.split("-")[4] # для чего, например при использовании одной и той же клавиатуры для разных сцен. Здесь нужно уметь удалять из отмеченных из сцены поиска и из сцены отмеченные
    isMarked = actions[action] # True или False - книги в списке отобрана или нет. Какое свойство нужно применить состоянию участия книги в списке отмеченные

    if forWhat == 'search':
        books = await db.readResult(user_id)  # все книги
        books[currentPage]['isMarked'] = isMarked # записываем значение отмеченности текущей книги
        await db.writeResult(user_id, books)  # записываем все книги пользователя в БД
        id_book = books[currentPage]['id'] # id книги для отбора для заказа(добавление в "корзину")

    info = await db.readUserInfo(user_id)
    name = info[0]
    id = info[1]
    obj = await AsyncApiClient.create(id, name)
    result = await obj.markBook(markDoc, isMarked) # удаление или добавление из списка "отмеченные"
    await obj.closeSession()

    if forWhat == 'listMarked':
        if action == 'update' or user_id not in markedBooksAllUsers.keys():
            info = await db.readUserInfo(user_id)
            name = info[0]
            id = info[1]
            obj = await AsyncApiClient.create(id, name)
            books = await obj.markedBooks()
            await obj.closeSession()
            markedBooksAllUsers[user_id] = books
            currentPage = 0
            id_book = books[currentPage]['id']
        else:
            markedBooksAllUsers[user_id][currentPage]['isMarked'] = isMarked
            books = markedBooksAllUsers[user_id]
            id_book = books[currentPage]['id']  # id книги для отбора для заказа(добавление в "корзину")
        length = len(books)
        await callback.message.edit_text(f'Страница {currentPage + 1}\n{books[currentPage]['book']}', reply_markup=kb.markedKb(id_book, markDoc, isMarked, length, current=currentPage))

    elif forWhat == 'search':
        length = len(books)
        await callback.message.edit_text(callback.message.text, reply_markup=kb.startKb(id_book, markDoc, isMarked, length, current=currentPage))

    if result and isMarked:
        await callback.answer('Книга отмечена')
    else:
        await callback.answer('Книга удалена из отмеченных')


# хэндлеры главного меню
@router.callback_query(F.data.startswith("receivedBooks_")) # полученные книги
async def callbacks_received_books(callback: types.CallbackQuery):
    currentPage = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    if user_id not in received_books.keys():
        info = await db.readUserInfo(user_id)
        name = info[0]
        id = info[1]
        obj = await AsyncApiClient.create(id, name)
        books = await obj.receivedBooks()
        await obj.closeSession()
    else:
        books = received_books[user_id]
   #  print(books)
    if currentPage > len(books)-1:
        currentPage = 0
    elif currentPage == -1:
        currentPage = len(books)-1
    received_books[user_id] = books
    book = books[currentPage]
    text = f'<b>Номер:</b> {book['number']}\nШтрих код: {book['barcode']}\n\nОписание: {book['bibliographic']}\n\nПункт книговыдачи: {book['PK']}\n\n<b>Дата выдачи:</b> {book['date_issue']}\n<b>Дата возврата:</b> {book['date_return']}'
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb.inMenu(books, currentPage))
    # await callback.answer('Пока данный раздел недоступен', show_alert=True)

@router.callback_query(F.data == "ordered_books") # заказанные книги
async def callbacks_ordered_books(callback: types.CallbackQuery):
    await callback.answer('Данный раздел пока недоступен', show_alert=True)

@router.callback_query(F.data.startswith('unSelect_'))
async def callbacks_unSelect(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    info = await db.readUserInfo(user_id)
    name = info[0]
    id = info[1]
    id_book = callback.data.split("_")[1]
    obj = await AsyncApiClient.create(id, name)
    result = await obj.unSelectBook(id_book)
    if result == 'ok':
        await callback.answer('Удалено')
        await callbacks_selected_books(callback)
        
    await obj.closeSession()

@router.callback_query(F.data.startswith("selectedBooks_")) # отобранные книги
async def callbacks_selected_books(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in selectedBooks.keys() or callback.data.split("_")[1] == 'update':
        currentPage = 0
        info = await db.readUserInfo(user_id)
        name = info[0]
        id = info[1]
        obj = await AsyncApiClient.create(id, name)
        books = await obj.selectedBooks()
        await obj.closeSession()
    else:
        books = selectedBooks[user_id]
        currentPage = int(callback.data.split("_")[1])

    if len(books) == 0:
        await callback.answer('У вас нет отобранных для заказа книг :(', show_alert=True)
        return
    if currentPage > len(books)-1:
        currentPage = 0
    elif currentPage < 0:
        currentPage = len(books)-1
    selectedBooks[user_id] = books
    num = selectedBooks[user_id][currentPage]['num']
    about = selectedBooks[user_id][currentPage]['total']
    id = selectedBooks[user_id][currentPage]['id']
    length = len(selectedBooks[user_id])
    text = f"№: {num}\n{about}"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb.selectedBooks(currentPage, length, id))
    # await callback.answer('Пока данный раздел недоступен', show_alert=True)

@router.callback_query(F.data.startswith("markedBooks_")) # отмеченные книги
async def callbacks_marked_books(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]
    if action == 'update' or user_id not in markedBooksAllUsers.keys():

        info = await db.readUserInfo(user_id)
        name = info[0]
        id = info[1]
        obj = await AsyncApiClient.create(id, name)
        books = await obj.markedBooks()
        await obj.closeSession()
        if books == False:
            await callback.answer('Нет отмеченных книг.', show_alert=True)
            return
        markedBooksAllUsers[user_id] = books
        currentPage = 0
        # print('Обновление/получение')
    else:
        currentPage = int(callback.data.split("_")[1])
        books = markedBooksAllUsers[user_id]
        # print('использование ОЗУ')
    if currentPage == -1:
        currentPage = len(books)-1
    elif currentPage > len(books)-1:
        currentPage = 0
    # print(books[currentPage])
    id_book = books[currentPage]['id']
    markDoc = books[currentPage]['markDoc']
    marked = books[currentPage]['isMarked']
    length = len(books)
    await callback.message.edit_text(f'Страница {currentPage + 1}\n{books[currentPage]['book']}', reply_markup=kb.markedKb(id_book, markDoc, marked, length, current=currentPage))







