from bs4 import BeautifulSoup


def parseBooks(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'pageTable'})
    lines = table.find_all('tr', class_=['docOdd', 'docEven'])
    listen = list()
    dictId = { # словарь для описания книги ключ - длина i, значение - id i.
        2: 1,
        4: 1,
        6: 3,
        8: 3,
        10: 3,
        12: 3,
    }
    for i in lines:
        forBook = len(i.find('table').find_all('td'))
        # print(forBook)
        d = {
            'number': i.find('td', {'class': 'nDoc'}).text.strip('.'),
            # 'keys_word': i.find('table').find_all('td')[5].text,
            'book': i.find('table').find_all('td')[dictId[forBook]].text.strip(),
            'markDoc': i.find('input', {'class': 'markDoc'}).get('id'),
            'isMarked': ('checked' in str(i.find('input')))
        }
        # print(i.find('table').find_all('td'))

        span_id = i.find('span', {'class': 'href selectToOrder'})
        if span_id:
            d['id'] = span_id.get('id')
        else:
            d['id'] = None
        # print(d)
        listen.append(d)
    return listen

def parseReceivedBooks(html):
    listen = list()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table').find_all('tr')[1:]
    for i in table:
        l = i.text.strip().split('\n')
        diction = {
            'number': l[0].strip(),
            'barcode': l[1].strip(),
            'bibliographic': l[2].strip(),
            'PK': l[3].strip(),
            'date_issue': l[4].strip(),
            'date_return': l[5].strip(),
        }
        listen.append(diction)
    return listen

def parseFund(html):
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')[1:]
    listen = list()
    for i in trs:
        d = {
            'name': i.find_all('td')[0].text,
            'total': i.find_all('td')[1].text,
            'available': i.find_all('td')[2].text,
        }
        d['availability'] = 'Отобрать' in str(i)
        if d['availability']:
            d['id'] = (i.find('span').get('id'))
        listen.append(d)
    # print(listen)
    return listen

def parseSelectedBooks(html):
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')[1:]
    listen = list()
    for i in trs:
        d = {
            'id': i.get('id'),
            'num': i.find_all('td')[0].text,
            'total': i.find_all('td')[1].text,
            'available': i.find_all('td')[2].text,
        }
        listen.append(d)
    # print(listen)
    return listen

def parseCountBooksMarked(html):
    if '<div id="ErrBox" title="Сообщение"></div>' in html:
        return False
    soup = BeautifulSoup(html, 'html.parser')
    result = int(soup.find('div', {'id': 'totalResult'}).text.split('-')[1])
    # print(result)
    return result


def parseMarkedSearchBooks(html):
    listen = list() # список словарей с информацией о книгах
    dictId = {  # словарь для описания книги ключ - длина i, значение - id i.
        2: 1,
        4: 1,
        6: 3,
        8: 3,
        10: 3,
        12: 3,
    }
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', {'class': 'pageTable'})
    for table in tables:
        lines = table.find_all('tr', class_=['docOdd', 'docEven'])
        for line in lines:
            forBook = len(line.find('table').find_all('td'))
            # print(forBook)
            d = {
                'number': line.find('td', {'class': 'nDoc'}).text.strip('.'),
                # 'keys_word': i.find('table').find_all('td')[5].text,
                'book': line.find('table').find_all('td')[dictId[forBook]].text.strip(),
                'markDoc': line.find('input', {'class': 'markDoc'}).get('id'),
                'isMarked': ('checked' in str(line.find('input')))
            }
            span_id = line.find('span', {'class': 'href selectToOrder'})
            if span_id:
                d['id'] = span_id.get('id')
            else:
                d['id'] = None
            listen.append(d)
    return listen
