import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_="common-table-div s-width").find('form', id="list_form1").find_all('table', class_="model-short-block")

    for div in divs:
        try:
            name = div.find('td', class_='model-short-info').find('a', class_='model-short-title no-u').find('span').text
        except:
           name = ''

        try:
            url = 'https://ek.ua' + div.find('td', class_='model-short-info').find('a', class_='model-short-title no-u').get('href')
        except:
            url = ''

        try:
            price1 = div.find('td', class_='model-hot-prices-td').find('div', class_='model-price-range').find('span').text
        except:
            price1 = ''

        try:
            price2 = div.find('td', class_='model-hot-prices-td').find('div', class_='model-price-range').find(
                'span').next.next.next.text
        except:
            price2 = ''

        data = {'name': name,
                'url': url,
                'price1': price1,
                'price2': price2}

        write_csv(data)


def write_csv(data):
    with open('ekua.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['name'],
                          data['url'],
                          data['price1'],
                          data['price2']))


def main():

    start = datetime.now()

    pattern = 'https://ek.ua/list/122/{}/'

    for i in range(0, 10):
        url = pattern.format(str(i))
        get_data(get_html(url))

    finish = datetime.now()
    result = finish - start
    print(str(result))


if __name__ == '__main__':
    main()