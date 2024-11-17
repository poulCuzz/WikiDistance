from itertools import count

import requests
from bs4 import BeautifulSoup

def get_urls(soup_data):
    # Znajdź wszystkie linki <a> na stronie
    all_links = soup_data.find_all('a', href=True)
    # Filtruj linki, aby pominąć te, które prowadzą do bieżącej strony
    # filtered_links = [link for link in all_links if first_word not in link['href']] <-- filtr do poprawy
    for link in all_links:
        print(filter_wiki_url(link['href']))

def filter_wiki_url(link):
    base_url = "https://pl.wikipedia.org"
    # Sprawdzamy, czy link zaczyna się od "/wiki"
    if link.startswith('/wiki'):
        return base_url + link
    elif link.startswith('http'):
        return link
    return None

def get_all_links(body_data):
    all_links = []
    for link in body_data.find_all('a', href=True):
        filtered_link = filter_wiki_url(link['href'])
        if filtered_link is not None:
            all_links.append(filtered_link)
    return all_links
# test pull request
def is_word_on_page(body_data):
    all_links = get_all_links(body_data)
    counter = 0
    found = False
    for link in all_links:
        print(f'counter = {counter}')
        counter += 1
        page_second = requests.get(link)
        soup_second = BeautifulSoup(page_second.text, 'html.parser')
        body_second = soup_second.find('div', id='bodyContent')
        if second_word in body_second.get_text():
            found = True
            break
    return found

URL = "https://pl.wikipedia.org/wiki/"
baseURL = "https://pl.wikipedia.org"
first_word = input("Pierwsze słowo: ")
second_word = input("Drugie słowo: ")
page = requests.get(URL + first_word)
soup = BeautifulSoup(page.text, 'html.parser')
body = soup.find('div', id='bodyContent')

if second_word in body.get_text():
    print(f"Distance between {first_word} and {second_word} is 1")
elif is_word_on_page(body):
    print(f"Distance between {first_word} and {second_word} is 2")
else:
        print('nie znaleziono słowa na zadnym linku, konieczne jest ponowne szukanie linków zaczynając od linku 1 na stronie body')



