from bs4 import BeautifulSoup
import urllib.request


req = urllib.request.urlopen('https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python')
html = req.read()

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


f = open('vacancy.txt', 'w', encoding='utf-8')
i=1
for item in res:
    f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
    i += 1

f.close()