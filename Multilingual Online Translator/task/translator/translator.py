import requests
from bs4 import BeautifulSoup
from http.client import responses

headers = {'User-Agent': 'Safari/15.0'}


def get_translations(soup) -> list:
    tag_attributes = {"id": "translations-content", "class": "wide-container"}
    return [el.text.strip("\n") for el in soup.find_all("div", tag_attributes)][0].split()


def get_examples(soup) -> list:
    bs4_tag_object = soup.find('section', id="examples-content")
    span_tags = bs4_tag_object.find_all('span', class_="text")
    return [element.text.strip() for element in span_tags]


def main():
    welcome_message = 'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:\n'
    target_language = input(welcome_message).lower()
    supported_languages = {"en": "english",
                           "fr": "french"}

    if target_language not in supported_languages:
        print("Incorrect option provided... starting over.")
        return main()

    else:
        input_language = supported_languages['en'] if target_language == "fr" else supported_languages['fr']
        word = input("Type the word you want to translate:\n")

        confirmation_message = f'You chose "{supported_languages[target_language]}" as a language to translate "{word}".'
        print(confirmation_message)

        page = requests.get(
            f"https://context.reverso.net/translation/{input_language}-{supported_languages[target_language]}/{word}",
            headers=headers)

        if not page.status_code == 200:
            return main()
        print(page.status_code, responses[page.status_code])
        soup = BeautifulSoup(page.content, "html.parser")
        translated_list, examples = \
            get_translations(soup), get_examples(soup)

        print(f"\n{supported_languages[target_language].capitalize()} Translations:")
        print(*translated_list, sep="\n")
        print(f"\n{supported_languages[target_language].capitalize()} Examples:")
        print(*examples, sep='\n')


if __name__ == "__main__":
    main()
