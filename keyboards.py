from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Полученные книги', callback_data='receivedBooks_0'))
    builder.row(types.InlineKeyboardButton(text='Заказанные книги', callback_data='ordered_books'))
    builder.row(types.InlineKeyboardButton(text='Отобранные книги', callback_data='selectedBooks_update'))
    builder.row(types.InlineKeyboardButton(text='Отмеченные книги', callback_data='markedBooks_update'))
    return builder.as_markup()

def inMenu(books, currentPage):
    builder = InlineKeyboardBuilder()
    if len(books) > 1:
        builder.add(types.InlineKeyboardButton(text="<--", callback_data=f"receivedBooks_{currentPage - 1}"))
        builder.add(types.InlineKeyboardButton(text="-->", callback_data=f"receivedBooks_{currentPage + 1}"))
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='start'))
    return builder.as_markup()

def startKb(id_book, markDoc, marked, length, current=0):
    builder = InlineKeyboardBuilder()
    if not marked:
        builder.add(types.InlineKeyboardButton(text="Отметить", callback_data=f"markDoc-add-{markDoc}-{current}-search"))
    else:
        builder.add(types.InlineKeyboardButton(text="Убрать из отмеченных", callback_data=f"markDoc-del-{markDoc}-{current}-search"))
    if id_book != None:
        builder.row(types.InlineKeyboardButton(text="Отобрать для заказа", callback_data=f"toorder-{id_book}-{current}-search"))
    if length != 1:
        builder.row(types.InlineKeyboardButton(text="<--", callback_data=f"nextpage_{current-1}"))
        builder.add(types.InlineKeyboardButton(text="-->", callback_data=f"nextpage_{current+1}"))
    return builder.as_markup()


def markedKb(id_book, markDoc, marked, length, current=0):
    builder = InlineKeyboardBuilder()
    if not marked:
        builder.add(types.InlineKeyboardButton(text="Отметить", callback_data=f"markDoc-add-{markDoc}-{current}-listMarked"))
    else:
        builder.add(types.InlineKeyboardButton(text="Убрать из отмеченных", callback_data=f"markDoc-del-{markDoc}-{current}-listMarked"))
    if id_book != None:
        builder.row(types.InlineKeyboardButton(text="Отобрать для заказа", callback_data=f"toorder-{id_book}-{current}-listMarked"))
    if length != 1:
        builder.row(types.InlineKeyboardButton(text="<--", callback_data=f"markedBooks_{current-1}"))
        builder.add(types.InlineKeyboardButton(text="-->", callback_data=f"markedBooks_{current+1}"))
    # print(length)
    builder.row(types.InlineKeyboardButton(text="В меню", callback_data="start"))
    return builder.as_markup()


def selectedBooks(currentPage, length, id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Убрать из отобранных', callback_data=f'unSelect_{id}'))
    if length > 1:
        builder.row(types.InlineKeyboardButton(text="<--", callback_data=f"selectedBooks_{currentPage - 1}"))
        builder.add(types.InlineKeyboardButton(text="-->", callback_data=f"selectedBooks_{currentPage + 1}"))
    print(id)
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='start'))
    return builder.as_markup()



def funds(funds, current):
    builder = InlineKeyboardBuilder()
    for fund in funds:
        if fund['availability']:
            builder.add(types.InlineKeyboardButton(text=fund['name'], callback_data=f'finorder-{fund["id"]}'))
    builder.row(types.InlineKeyboardButton(text='Вернуться', callback_data=f'nextpage_{current}'))
    return builder.as_markup()


def fundsMarkedList(funds, current):
    builder = InlineKeyboardBuilder()
    for fund in funds:
        if fund['availability']:
            builder.add(types.InlineKeyboardButton(text=fund['name'], callback_data=f'finorder-{fund["id"]}'))
    builder.row(types.InlineKeyboardButton(text='Вернуться', callback_data=f'markedBooks_{current}'))
    return builder.as_markup()


def accpetPdn():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="✅ Принимаю", callback_data="accept_pdn"))
    return builder.as_markup()


def finOrder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Вернуться', callback_data='nextpage_0'))
    return builder.as_markup()