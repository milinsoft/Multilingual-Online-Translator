import sys

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Safari/15.0'}


def get_translations(soup) -> list:
    tag_attributes = {"id": "translations-content", "class": "wide-container"}
    try:
        return [el.text.strip("\n") for el in soup.find_all("div", tag_attributes)][0].split()
    except IndexError:
        pass


def get_examples(soup) -> list:
    bs4_tag_object = soup.find('section', id="examples-content")
    try:
        span_tags = bs4_tag_object.find_all('span', class_="text")
        return [element.text.strip() for element in span_tags]
    except AttributeError:
        pass


def assign_language(mode: str, languages: tuple) -> str:
    message = {"in": "Type the number of your language:\n",
               "out": "Type the number of language you want to translate to or '0' to translate to all languages:\n",
               }[mode]

    try:
        number = int(input(message))
        assert 1 <= number <= 13 if mode == "in" else 0 <= number <= 13
    except (ValueError, AssertionError):
        print("PROVIDE THE NUMBER, NOTHING ELSE.")
        return assign_language(mode, languages)
    return languages[number - 1].lower() if number != 0 else "all"


def save_translations(wrd, ):
    ...




def main():

    def translate(target_language):
        page = requests.get(
        f"https://context.reverso.net/translation/{input_language}-{target_language.lower()}/{word}",
        headers=headers)

        if not page.status_code == 200:
            return main()

        soup = BeautifulSoup(page.content, "html.parser")
        translated_list, examples = \
            get_translations(soup), get_examples(soup)



        if translated_list:
            with open(f"{word}.txt", 'a+') as file:
                print(f"\n{target_language} Translations:")
                print(*translated_list, sep="\n")
                print(f"\n{target_language} Examples:")
                print(*examples, sep='\n')


                print(f"\n{target_language} Translations:", file=file)
                print(*translated_list, sep="\n", file=file)
                print(f"\n{target_language} Examples:", file=file)
                print(*examples, sep='\n', file=file)


    supported_languages = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                           'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')

    print("Hello, you're welcome to the translator. Translator supports:\n")
    for n, language in enumerate(supported_languages, start=1):
        print(f"{n}. {language}")

    input_language = assign_language("in", supported_languages)
    target_language = assign_language("out", supported_languages)

    word = input("\nType the word you want to translate:\n").lower()

    if target_language != "all":
        return translate(target_language)
    else:
        for language in supported_languages:
            translate(language)
            #print(language)






if __name__ == "__main__":
    main()
