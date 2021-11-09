from bs4 import BeautifulSoup
import requests
from requests.api import head

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    }

s = requests.Session()
html = s.get(url='https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python', headers=headers).text


with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html)

soup = BeautifulSoup(html, 'html.parser')

vacancy = soup.find_all('div', class_='vacancy')


res = []

for i in vacancy:
    title = i.find('a', class_='vt').get_text()
    desc = i.find('div', class_='sh-info').get_text(strip=True)
    href = i.find('a', class_='vt').get('href')
    res.append({
        'title': title,
        'desc': desc,
        'href': href,
    })

with open('vacancy.txt', 'w', encoding='utf-8') as f:   
    i=1
    for item in res:
        f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
        i += 1
