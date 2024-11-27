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

def main_function(main_link, counter=1, max_depth=5):
    """
    Rekurencyjna funkcja do wyznaczenia odległości między słowami w sensie logicznym na stronach internetowych.

    Args:
        main_link (str): Link do strony, od której rozpoczyna się wyszukiwanie.
        counter (int): Licznik poziomu wyszukiwania.
        max_depth (int): Maksymalna dozwolona głębokość wyszukiwania.

    Returns:
        int: Odległość logiczna między słowami lub -1, jeśli słowo nie zostanie znalezione.
    """
    # Sprawdza, czy przekroczono maksymalną głębokość
    if counter > max_depth:
        print("Osiągnięto maksymalną głębokość wyszukiwania.")
        return -1

    # Pobiera treść artykułu
    body = find_article_content(main_link)
    if isinstance(body, str):
        print(f"Treść strony: {body}")
        return -1  # Zwrot -1 w przypadku błędnej treści

    # Sprawdza, czy drugie słowo jest w treści
    if second_word in body.get_text():
        return counter
    counter += 1
    # Sprawdza czy jest w którymś z linków
    print(f"Poziom wyszukiwania: {counter}")
    if is_word_on_any_page(main_link):
        return counter
    counter += 1
    # Przechodzi przez linki na bieżącej stronie i szuka głębiej
    for link in get_all_links(body):
        print(f"Poziom wyszukiwania: {counter}, Przeszukiwany link: {link}")
        # Sprawdź, czy drugie słowo jest na tej stronie
        if is_word_on_any_page(link):
            return counter
    loop_counter = 1
    # Rekurencyjnie przeszukuje każdy link
    for link in get_all_links(body):
        loop_counter += 1
        result = main_function(link, counter + 1, max_depth)
        if result != -1:  # Jeśli znaleziono słowo, zwracamy wynik
            return result

    # Jeśli nie znaleziono słowa w tej gałęzi, zwraca -1
    return -1


print(f"Odległośc logiczna między słowami: '{first_word}', '{second_word}' wynosi {main_function((URL + first_word), main_counter)}")

