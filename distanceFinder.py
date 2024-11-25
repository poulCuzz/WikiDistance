import requests
from bs4 import BeautifulSoup


def filter_wiki_url(link):
    base_url = "https://pl.wikipedia.org"
    # Sprawdzenie, czy link zaczyna się od "/wiki"
    if link.startswith('/wiki'):
        return base_url + link # zwracamy pełny link
    # Sprawczenie czy url prowadzi do strony z wikipedii
    elif link.startswith('http') and 'wikipedia.org/wiki' in link:
        return link
    return None

# Funkcja zwraca liste linków z elementu body
def get_all_links(body_data):
    all_links = []
    for link in body_data.find_all('a', href=True):
        filtered_link = filter_wiki_url(link['href'])
        if filtered_link is not None:
            all_links.append(filtered_link)
    return all_links

# Funckja szuka elementu o id = 'mw-content-text' i wyszukuje nagłówki i paragrafy aby pominąć treści wyrwane z kontekstu zadania
def find_article_content(url_link):
    try:
        # Pobiera stronę
        response = requests.get(url_link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Znajdeje główną sekcję treści
        content_div = soup.find('div', id='mw-content-text')
        if not content_div:
            print("Nie znaleziono głównej sekcji treści.")
            return None

        # Inicjalizuje listę wyników
        article_content = content_div.find_all(['h2', 'h3', 'p', 'ul', 'ol'])

        combined_tag = soup.new_tag('div')
        for element in article_content:
            combined_tag.append(element)

        return combined_tag

    except requests.exceptions.RequestException as e:
        return f"Błąd podczas pobierania strony: {e}"

def is_word_on_any_page(main_link):
    body_data = find_article_content(main_link)
    if isinstance(body_data, str):
        print(body_data)
        return body_data
    all_links = get_all_links(body_data)
    link_counter = 0
    found = False
    for link in all_links:
        # print(f'link_counter = {link_counter}')
        print(link)
        link_counter += 1
        page_second = requests.get(link)
        soup_second = BeautifulSoup(page_second.text, 'html.parser')
        body_second = soup_second.find('div', id='bodyContent')
        if body_second is None:
            print(f"Warning: Body for link {main_link} is None.")
            return False  # Możesz zwrócić False lub odpowiednią wartość w zależności od logiki
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

    body = find_article_content(main_link)
    if isinstance(body, str):
        print(body)
        return body
    if second_word in body.get_text():
        return 1
    elif is_word_on_any_page(main_link):
        return 2
    else:
        result = 0
        for link in get_all_links(body):
            print(f'main counter -> {counter}')
            counter += 1
            result += main_function(link, counter) + 2
            if result is None:  # Sprawdzenie, czy wynik rekurencji to None
                return 0  # Zwracam 0, jeśli wynik jest None
        return result




print(f"Odległośc logiczna między słowami: '{first_word}', '{second_word}' wynosi {main_function((URL + first_word), main_counter)}")

