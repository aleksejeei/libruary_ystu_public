import aiohttp


async def checkAuth(rdr_id, rdr_name):
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
    r = await session.post(urlAuth, data=data, headers=headers)
    result = (await r.text())
    await session.close()
    # print(result)
    if result == 'ok':
        return True
    return False