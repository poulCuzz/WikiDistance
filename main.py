import requests
from bs4 import BeautifulSoup

def print_urls(soup_data):
    # Znajdź wszystkie linki <a> na stronie
    all_links = soup_data.find_all('a', href=True)
    # Filtruj linki, aby pominąć te, które prowadzą do bieżącej strony
    filtered_links = [link for link in all_links if first_word not in link['href']]
    for link in filtered_links:
        print(filter_wiki_url(link['href']))

def filter_wiki_url(link):
    base_url = "https://pl.wikipedia.org"
    # Sprawdzamy, czy link zaczyna się od "/wiki"
    if link.startswith('/wiki'):
        return base_url + link
    elif link.startswith('http'):
        return link
    return None

URL = "https://pl.wikipedia.org/wiki/"
baseURL = "https://pl.wikipedia.org"
first_word = input("Pierwsze słowo: ")
page = requests.get(URL + first_word)
soup = BeautifulSoup(page.text, 'html.parser')
body = soup.find('div', id='bodyContent')
other_meanings = soup.find('a', title="Inne znaczenia")
if soup.find('a', title=lambda t: t and 'ujednoznacznienie' in t):
    #sprawdzenie czy są inne znaczenia słowa:
    if other_meanings:
        print("są różne znaczenia, wybierz z poniższych opcji:")
        first_span = other_meanings.find_parent('span')
        second_span = first_span.find_next_sibling('span')
        # Znajdujemy link z "ujednoznacznienie" w title
        link_to_disambiguation = second_span.find('a', title=lambda t: t and 'ujednoznacznienie' in t)
        if link_to_disambiguation:
            page_with_others = requests.get(baseURL + link_to_disambiguation['href'])
            soup_with_others = BeautifulSoup(page_with_others.text, 'html.parser')
            block_with_others = soup_with_others.find('div', class_ = "mw-content-ltr mw-parser-output")
            # Szukamy wszystkich elementów li, a następnie linków a w nich
            counter = 1
            url_list = [URL + first_word]
            print(f"0 :: Tytuł: {first_word}, Link: {url_list[0]}")
            for li in block_with_others.find_all('li'):
                link = li.find('a', href=True)
                if link:
                    url = link['href']
                    title = link['title']
                    url_list.append(baseURL + url)
                    print(f'{counter} :: Tytuł: {title}, Link: {baseURL + url}')
                    counter += 1
            url_number = int(input('podaj numer: '))
            chosen_page = requests.get(url_list[url_number])
            #aktualizacja danych
            soup = BeautifulSoup(chosen_page.text, 'html.parser')
            body = soup.find('div', id='bodyContent')

            print_urls(body)
        else:
            other_links = second_span.find_all('a')
            counter = 1
            url_list = [URL + first_word]
            print(f'0: {first_word}')
            for link in other_links:
                print(f"{counter}: {link.text}")
                url_list.append(URL + link.get_text())
                counter += 1
            url_number = int(input('podaj numer: '))
            chosen_page = requests.get(url_list[url_number])
            # aktualizacja danych
            soup = BeautifulSoup(chosen_page.text, 'html.parser')
            body = soup.find('div', id='bodyContent')
            print_urls(body)
    else:
        print_urls(body)

else:
    # Szukamy wszystkich elementów li, a następnie linków a w nich
    counter = 1
    url_list = []

    for li in body.find_all('li'):
        link = li.find('a', href=True)
        if link:
            url = link['href']
            title = link['title']
            url_list.append(baseURL + url)
            print(f'{counter} :: Tytuł: {title}, Link: {baseURL + url}')
            counter += 1
    url_number = int(input('podaj numer: '))
    chosen_page = requests.get(url_list[url_number - 1])
    # aktualizacja danych
    soup = BeautifulSoup(chosen_page.text, 'html.parser')
    body = soup.find('div', id='bodyContent')

    print_urls(body)


