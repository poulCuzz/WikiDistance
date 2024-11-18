import requests
from bs4 import BeautifulSoup


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

def find_body(url_link):
    page = requests.get(url_link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find('div', id='bodyContent')

def is_word_on_any_page(main_link):
    body_data = find_body(main_link)
    all_links = get_all_links(body_data)
    link_counter = 0
    found = False
    for link in all_links:
        print(f'link_counter = {link_counter}')
        link_counter += 1
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
main_counter = 1

def main_function(main_link, counter):

    body = find_body(main_link)
    if second_word in body.get_text():
        return 1
    elif is_word_on_any_page(main_link):
        return 2
    else:
        for link in get_all_links(body):
            print(f'main counter -> {counter}')
            counter += 1
            if counter > 5:
                print("przeciążenie, koniec programu")
                break
            return main_function(link, counter) + 2


print(f"Odległośc logiczna między słowami: '{first_word}', '{second_word}' wynosi {main_function((URL + first_word), main_counter)}")

