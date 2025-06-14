conf = """Политика конфиденциальности Telegram-бота "Библиотека ЯГТУ"

<b>1. Общие положения</b>
1.1. Настоящая Политика определяет порядок обработки персональных данных пользователей бота.
1.2. Использование Бота означает <b>безоговорочное согласие</b> пользователя с данной Политикой.
1.3. Бот <b>не является официальным сервисом ЯГТУ</b> и действует независимо от учебного заведения.

<b>2. Состав персональных данных</b>
Обработке подлежат:

<b>Для авторизации в библиотеке ЯГТУ:</b>
• Логин от учетной записи электронной библиотеки
• Номер читательского билета

<b>Технические данные:</b>
• Telegram user ID
• История запросов к Боту

<b>3. Цели обработки данных</b>
3.1. Данные используются <b>исключительно</b> для:

Авторизации в системе электронной библиотеки ЯГТУ

• Оформления заказа книг через Бота

• Технической поддержки и улучшения функционала

• Предотвращения мошенничества

<b>4. Правовые основания обработки</b>
4.1. Обработка осуществляется на основании:

<b>ст. 6 152-ФЗ РФ</b> – согласие субъекта ПДн

4.2. Пользователь дает согласие через явное подтверждение (кнопка "✅ Принимаю" при первом запуске).

<b>5. Сроки хранения данных</b>
5.1. Данные хранятся до момента отзыва согласия пользователем.

<b>6. Защита данных</b>
6.1. Применяемые меры:

Шифрование AES-256 для баз данных

Ограниченный доступ (только для разработчика)
6.2. В случае утечки:

Уведомление пользователей в течение 72 часов

Блокировка compromised-данных

<b>7. Передача данных третьим лицам</b>
7.1. Данные <b>не передаются</b> коммерческим организациям.
7.2. Исключения:

По запросу судебных органов РФ

Для интеграции с официальным API библиотеки ЯГТУ (если применимо)

<b>8. Права пользователя (ст. 14 152-ФЗ)</b>
Пользователь имеет право:
8.1. <b>Отозвать согласие</b> через команду /delete_me.

<b>9. Ответственность</b>
9.1. Разработчик не несет ответственности за:

• Блокировку аккаунта библиотекой ЯГТУ

• Утечки данных из-за действий хакеров

• Некорректную работу парсинга

<b>10. Контакты</b>
По вопросам персональных данных обращайтесь:

Telegram: @libruary_ystu
"""


acceptPdn = """Используя Бота, вы подтверждаете, что:

1. Даете согласие на обработку: логина(фамилии), номера читательского билета и технических данных (User ID).

2. Ознакомились с Политикой конфиденциальности.
"""

postLogin = """Вы успешно авторизовались. Можете приступить к поиску книг :)\n/help - Для получения инструкции"""

help = """Для начала нажмите /start для входа в меню и нажмите соответствующую кнопку.

1. 🔍 Чтобы произвести поиск книги, просто напишите её название или автора в чат. Рекомендуется как можно точнее указывать данные книги. 🔍

2. ☑️ Книги можно отметить или отобрать для заказа, если эти функции доступны для определённых книг. Потом их можно будет найти в соответствующих разделах меню и при желании редактировать эти списки. ☑️

3. ✅ При отборе книги для заказа Вам нужно будет нажать "отобрать для заказа" и выбрать один из доступных пунктов книговыдачи(ПК). Если ПК отсутствует для выбора, значит он недоступен. ✅"""