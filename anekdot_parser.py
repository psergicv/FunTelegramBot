import requests
import json
from bs4 import BeautifulSoup


def get_page(url):
    r = requests.get(url)
    return r.text


def get_page_number(page):
    soup = BeautifulSoup(page, 'lxml')

    block = soup.find('div', class_='pagin')

    all_urls = block.find_all('a')
    page_numbers_list = []
    for url in all_urls:
        page_number = url.text
        page_numbers_list.append(int(page_number))

    return max(page_numbers_list)


def get_data(page):
    soup = BeautifulSoup(page, 'lxml')

    anekdots = dict()
    anek_id = 0
    all_anekdots = soup.find_all('div', class_='tecst')
    for anekdot in all_anekdots:
        anek_id += 1
        anekdot_text = anekdot.text.split("\n")[1].strip()
        anekdots[anek_id] = {
            anek_id: anekdot_text
        }

    return anekdots


def save_data(data):
    with open('anekdot_db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    initial_url = "https://anekdotbar.ru/page/1/"
    initial_page = get_page(initial_url)
    pg_nr = get_page_number(initial_page)

    anek_db = dict()
    for page_nr in range(1, pg_nr):
        print(f"Starting to parse page {page_nr}")
        url = f"https://anekdotbar.ru/page/{page_nr}/"
        page = get_page(url)
        data = get_data(page, page_nr)
        anek_db[page_nr] = data
        print(f"Page {page_nr} out of {pg_nr} parsed")
    save_data(anek_db)


if __name__ == '__main__':
    main()
