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
            title = i.find('a', class_='profile').get_text()
            desc = i.find('div', class_='list-jobs__description').get_text(strip=True).replace('\r\n', '')
            href = 'https://djinni.co/' + i.find('a', class_='profile').get('href')
            res.append({
                'title': title,
                'desc': desc,
                # 'details':details,
                'href': href,
            })


        return soup.find('ul', class_='pager').find_all('a')[-1].text
    
    x = 1
    res = []
    page_url = 'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp'
    while True:
        if get_info_from_page(page_url) != 'наступна →':
            return res
        x += 1
        get_info_from_page(f'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp&page={x}')
        page_url = f'https://djinni.co/jobs/keyword-python/kyiv/?exp_level=no_exp&page={x}'



def main():
    dou_vacancy = get_dou_vacancy()
    djinni_vacancy = get_djinni_vacancy()

    with open('vacancy.txt', 'w', encoding='utf-8') as f:   
        i=1
        f.write('\n\nFrom dou.ua\n\n')
        for item in dou_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1
        f.write('-'*50)
        f.write('\n\nFrom djinni.co\n\n')
        for item in djinni_vacancy:
            f.write(f'{i}. {item["title"]}\n {item["desc"]}\n {item["href"]}\n\n')
            i += 1
        f.write('-'*50)


if __name__ == '__main__':
    main()