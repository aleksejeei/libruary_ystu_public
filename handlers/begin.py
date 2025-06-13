from aiogram.filters.command import Command
from aiogram import F, types, Router
import accepts
import keyboards as kb
import db.control as db
from parser.check_auth import checkAuth
import filters.accept as acceptFilter
import filters.authorize as authorize

router = Router()

@router.message(acceptFilter.CheckAcceptFilter()) # ловим все сообщения от пользователей, которые не приняли пользовательское соглашение и пытаются написать боту сообщение
async def check_accept(message: types.Message):
    await message.answer(accepts.conf, parse_mode="HTML")
    await message.answer(accepts.acceptPdn, reply_markup=kb.accpetPdn())

@router.callback_query(F.data == "accept_pdn") # хэндлер принятия соглашений использования
async def callbacks_accept(callback: types.CallbackQuery):
    await db.acceptPrivacyWrite(callback.from_user.id)
    acceptFilter.accepted[callback.from_user.id] = 1
    await callback.message.edit_text(text=f'{accepts.acceptPdn}\n\n✅ Вы приняли соглашение. ✅ \n\nТеперь необходимо авторизоваться, используя логин(фамилию) и номер читательского билета ЯГТУ. Используйте команду вида:\n/login <логин> <номер читательского билета>\n\nПример:\n/login Иванов 9D9S9DS')
    await callback.answer()

@router.callback_query(acceptFilter.CheckAcceptFilterCallback()) # принимаем все callback если не принято пользовательское соглашение
async def check_callback(callback: types.CallbackQuery):
    await callback.answer('Не подписано пользовательское соглашение', show_alert=True)
    await callback.message.answer(accepts.conf, parse_mode="HTML")
    await callback.message.answer(accepts.acceptPdn, reply_markup=kb.accpetPdn())

@router.message(Command("delete_me"))
async def delete_me(message: types.Message):
    user_id = message.from_user.id
    try:
        del acceptFilter.accepted[user_id]
    except:
        pass
    try:
        del authorize.auth[user_id]
    except:
        pass
    await db.deleteUserId(user_id)
    # acceptFilter.accepted[user_id] = 0
    await message.answer('Ваши данные были удалены из системы :(')

@router.message(Command("login"))
async def cmd_login(message: types.Message):
    try:
        name = message.text.split()[1]
        id = message.text.split()[2]
    except:
        await message.answer('Ошибка :(\nВозможно неверные данные авторизации.')
        return

    check = await checkAuth(id, name)

    if check:
        await db.writeLoginReadId(message.from_user.id, name, id)
        authorize.auth[message.from_user.id] = False
        await message.answer(accepts.postLogin, parse_mode="HTML")
    else:
        await message.answer('Ошибка :(\nВозможно неверные данные авторизации.')

@router.message(authorize.AuthFilter())
async def catchUnAuth(message: types.Message):
    text = '''Необходимо авторизоваться, используя логин(фамилию) и номер читательского билета ЯГТУ. Используйте команду вида:
/login [логин] [номер читательского билета]

Пример:
/login Иванов 9D9S9DS'''
    await message.answer(text, parse_mode="HTML")

@router.callback_query(authorize.AuthFilterCallback())
async def catchUnAuthCallback(callback: types.CallbackQuery):
    await callback.answer('Вы не авторизовались!')
    text = '''Необходимо авторизоваться, используя логин(фамилию) и номер читательского билета ЯГТУ. Используйте команду вида:
/login [логин] [номер читательского билета]

Пример:
/login Иванов 9D9S9DS'''
    await callback.message.answer(text, parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(accepts.help, parse_mode="HTML")