import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Safari/15.0'}


def get_translations(soup) -> list:
    tag_attributes = {"id": "translations-content", "class": "wide-container"}
    return [el.text.strip("\n") for el in soup.find_all("div", tag_attributes)][0].split()


def get_examples(soup) -> list:
    bs4_tag_object = soup.find('section', id="examples-content")
    span_tags = bs4_tag_object.find_all('span', class_="text")
    return [element.text.strip() for element in span_tags]


def assign_language(message: str, languages: tuple) -> str:
    try:
        number = int(input(message))
        assert 1 < number < 13
    except (ValueError, AssertionError):
        print("PROVIDE THE NUMBER, NOTHING ELSE.")
        return assign_language(message, languages)
    return languages[number-1].lower()


def main():
    supported_languages = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')

    print("Hello, you're welcome to the translator. Translator supports:\n")
    for n, language in enumerate(supported_languages, start=1):
        print(f"{n}. {language}")

    input_language = assign_language("Type the number of your language:\n", supported_languages)
    target_language = assign_language("Type the number of language you want to translate to:\n", supported_languages)

    word = input("\nType the word you want to translate:\n").lower()

    page = requests.get(
            f"https://context.reverso.net/translation/{input_language}-{target_language}/{word}",
            headers=headers)

    if not page.status_code == 200:
        return main()

    soup = BeautifulSoup(page.content, "html.parser")
    translated_list, examples = \
        get_translations(soup), get_examples(soup)

    print(f"\n{target_language} Translations:")
    print(*translated_list, sep="\n")
    print(f"\n{target_language} Examples:")
    print(*examples, sep='\n')


if __name__ == "__main__":
    main()
