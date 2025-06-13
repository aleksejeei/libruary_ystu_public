import aiohttp
import asyncio
from parser import parser
import os


class AsyncApiClient:
    def __init__(self, session):
        self.session = session
        self.urlGet = "http://www.ystu.ru:39445/megapro/Web"

    @classmethod
    async def create(cls, rdr_id, rdr_name):
        data = {'name': rdr_name, 'id': rdr_id}
        headers = {'Referer': 'http://www.ystu.ru:39445/megapro/Web',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Language': 'ru,en;q=0.9',
                   'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Accept-Encoding': 'gzip, deflate',
                   'Host': 'www.ystu.ru:39445',
                   'Origin': 'http://www.ystu.ru:39445',
                   }
        urlAuth = "http://www.ystu.ru:39445/megapro/Web/Home/RegRdr"
        session = aiohttp.ClientSession(headers=headers)
       # async with aiohttp.ClientSession(headers=headers) as session:
        r = await session.post(urlAuth, data=data, headers=headers)
        # print(await r.text(), data)
        return cls(session)


    async def findBooks(self, nameBook):  # поиск книг
        data = {
            'simpleCond': nameBook,
            'cond_words': 'all',
            'cond_match': 'right_truncate',
            'filter_dateTo': '',
            'sort': 'SORT1'
        }
        post = await self.session.post('http://www.ystu.ru:39445/megapro/Web/SearchResult/Simple', data=data)
        html = await post.text()
        # print(html)
        # return parser.parseBooks(html)
        return parser.parseMarkedSearchBooks(html)

    async def receivedBooks(self): # парсинг полученных книг
        url = 'http://www.ystu.ru:39445/megapro/Web/BookList/Hand'
        result = await self.session.get(url)
        result_text = await result.text()
        return parser.parseReceivedBooks(result_text)

    async def selectedBooks(self):
        url = 'http://www.ystu.ru:39445/megapro/Web/BookList/Selected'
        result = await self.session.get(url)
        result_text = await result.text()
        # print(parser.parseSelectedBooks(result_text))
        return parser.parseSelectedBooks(result_text)

    async def unSelectBook(self, id):
        url = f'http://www.ystu.ru:39445/megapro/Web/BookList/Del/{id}'
        result = await self.session.post(url)
        result_text = await result.text()
        print(result_text)
        return result_text
        # return 0


    async def markedBooks(self):
        url = 'http://www.ystu.ru:39445/megapro/Web/BookList/Marked'
        result = await self.session.get(url)
        result_html = await result.text()
        count = parser.parseCountBooksMarked(result_html)
        if not count:
            return False
        # print(count//20+1)
        for i in range(1, count//20+1):
            get_plus = await self.session.get(f'http://www.ystu.ru:39445/megapro/Web/SearchResult/ToPage/{i+1}')
            result_html += await get_plus.text()
        return parser.parseMarkedSearchBooks(result_html)

    async def getFundLib(self, book_id): # Получение доступных книжных фондов
        await self.findBooks('test')
        url = 'http://www.ystu.ru:39445/megapro/Web/SearchResult/GetAccTable'
        result = await self.session.post(url, data={'id': book_id})
        # print(21)
        return parser.parseFund(await result.text())

    async def toOrderBook(self, book_id): # отбор книг
        await self.getFundLib(book_id)
        url = 'http://www.ystu.ru:39445/megapro/Web/SearchResult/SelectBook'
        result = await self.session.post(url, data={'id': book_id})
        return (eval(await result.text()))

    async def markBook(self, markDoc, mark): # отметить книгу
        await self.findBooks('test')
        url = 'http://www.ystu.ru:39445/megapro/Web/SearchResult/MarkDoc'
        result = await self.session.post(url, data={'id': markDoc, 'mark': str(mark).lower()})
        # print("В коннекте:", str(mark).lower(), type(str(mark).lower()), await result.text())
        return (await result.text())

    async def closeSession(self): # закрыть сессию
        await self.session.close()

