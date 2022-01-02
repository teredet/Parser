from bs4 import BeautifulSoup
import requests


def get_html(url):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        }

    s = requests.Session()
    return s.get(url=url, headers=headers).text

def get_dou_vacancy():
    html = get_html('https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python&exp=0-1')
    soup = BeautifulSoup(html, 'lxml')
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

    return res


def get_djinni_vacancy():    
    
    def get_info_from_page(url_page):
        html = get_html(url_page)
        soup = BeautifulSoup(html, 'lxml')
        vacancy = soup.find_all('li', class_='list-jobs__item')

        for i in vacancy:
            title = i.find('a', class_='profile').get_text(strip=True)
            desc = i.find('div', class_='list-jobs__description').get_text(strip=True).replace('\r\n', '')
            href = 'https://djinni.co/' + i.find('a', class_='profile').get('href')
            res.append({
                'title': title,
                'desc': desc,
                'href': href,
            })

        try: 
            last_page = soup.find('ul', class_='pager').find_all('a')[-1].text
        except Exception:
            return 0 
        else:
            return last_page
    
    x = 1
    res = []
    page_url = 'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp'
    while True:
        if get_info_from_page(page_url) == 'наступна →':
            x += 1
            get_info_from_page(f'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp&page={x}')
            page_url = f'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp&page={x}'
        else:
            return res


def get_workua_vacancy(): 
    html = get_html('https://www.work.ua/jobs-kyiv-python/')
    soup = BeautifulSoup(html, 'lxml')
    pagination_count = int(soup.find('ul', class_='pagination').find_all('li')[-2].text)

    res = []

    for page in range(1, pagination_count+1):
        html = get_html(f'https://www.work.ua/jobs-kyiv-python/?page={page}')
        soup = BeautifulSoup(html, 'lxml')
        vacancy = soup.find_all('div', class_='job-link')

        for i in vacancy:
            title = i.find('h2').find('a').get_text()
            desc = i.find('p', class_='add-top-sm').get_text(strip=True).replace('\r\n', '')
            href = 'https://www.work.ua' + i.find('h2').find('a').get('href')
            res.append({
                'title': title,
                'desc': desc,
                'href': href,
            })

    return res


def get_rabotaua_vacancy():
    html = get_html('https://rabota.ua/zapros/junior-python-developer/%D0%BA%D0%B8%D0%B5%D0%B2')
    soup = BeautifulSoup(html, 'lxml')
    vacancy = soup.find_all('div', class_='card-body')
    
    res = []

    for i in vacancy:
        title = i.find('h2', class_='card-title').find('a').get_text()
        desc = i.find('div', class_='card-description').get_text(strip=True).replace('\r\n', '')
        href = 'https://rabota.ua' + i.find('h2', class_='card-title').find('a').get('href')
        res.append({
            'title': title,
            'desc': desc,
            'href': href,
        })

    return res


def main():
    dou_vacancy = get_dou_vacancy()
    djinni_vacancy = get_djinni_vacancy()
    workua_vacancy = get_workua_vacancy()
    rabotaua_vacancy = get_rabotaua_vacancy()

    with open('vacancy.txt', 'w', encoding='utf-8') as f:   
        strip = '-'*100 + '\n'

        i=1
        f.write(strip)
        f.write('From dou.ua (Python, < 1року, Київ)\n')
        f.write(strip)
        for item in dou_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1

        i=1
        f.write(strip)
        f.write('From djinni.co (Python, Київ, Без досвіду)\n')
        f.write(strip)
        for item in djinni_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1

        i=1
        f.write(strip)
        f.write('From work.ua (Python, Київ)\n')
        f.write(strip)
        for item in workua_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1
        
        i=1
        f.write(strip)
        f.write('From rabota.ua (Junior Python Developer, Київ)\n')
        f.write(strip)
        for item in rabotaua_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1
        f.write(strip)


if __name__ == '__main__':
    main()
    #get_workua_vacancy()