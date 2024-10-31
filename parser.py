import requests
from bs4 import BeautifulSoup as bs
import json

url = 'https://quotes.toscrape.com/page/'
class Scrape:
    def __init__(self, url: str):
        self.url = url

    def scraping(self):
        i = 1
        result = {}
        # создаём json-файл
        with open('data.json', 'w+', encoding = 'utf-8') as file:
            # цикл получает, обрабатывает и сохраняет в память информацию постранично
            while True:
                # получаем информацию со страницы
                response = requests.get(f'{url}{i}')
                # размечаем страницу с помощью beautyfulsoup4
                page_code = bs(response.text, 'html.parser')
                # ищем блоки с цититами на странице
                required_data = page_code.find_all('div', class_='quote')
                # если цитат нет - прерываем цикл
                if len(required_data) == 0:
                    break
                # иначе - продолжаем выполнение
                else:
                    data = {}
                    # перебираем блоки с цитатами
                    for index, item in enumerate(required_data):
                        number_on_page = {}
                        # выбираем нужные элементы и записываем в словарь number_on_page с информацией о цитате
                        number_on_page['text'] = item.find('span', class_='text').text.replace('\u201c', '').replace('\u201d', '')
                        number_on_page['author'] = item.find('small', class_='author').text
                        number_on_page['tags'] = []
                        for element in item.find_all('a', class_='tag'):
                            number_on_page['tags'].append(element.text)
                        # добавляем словарь number_on_page с порядковым номером в словарь data, в котором содеражится информация о цитатах с определённой страницы
                        data[f'text_{index+1}'] = number_on_page
                    # добавляем словарь data с порядковым номером страницы в итоговый словарь result
                    result[f'page_{i}'] = data
                    i+=1
            # выводим итоговые данные в file.json из словаря result
            json.dump(result, file, indent = 4)

scrape = Scrape(url)
scrape.scraping()