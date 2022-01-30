import sys
import requests
from bs4 import BeautifulSoup
from os.path import exists

headers = {'User-Agent': 'Safari/15.0'}


def translate_to_file(_input_language, _out_language, _word):
    def get_translations() -> list:
        tag_attributes = {"id": "translations-content", "class": "wide-container"}
        try:
            return [el.text.strip("\n") for el in soup.find_all("div", tag_attributes)][0].split()
        except IndexError:
            pass

    def get_examples() -> list:
        bs4_tag_object = soup.find('section', id="examples-content")
        try:
            span_tags = bs4_tag_object.find_all('span', class_="text")
            return [element.text.strip() for element in span_tags]
        except AttributeError:
            pass

    page = requests.get(
        f"https://context.reverso.net/translation/{_input_language}-{_out_language.lower()}/{_word}",
        headers=headers)

    if page.status_code != 200:
        return main()

    soup = BeautifulSoup(page.content, "html.parser")
    translated_list, examples = \
        get_translations(), get_examples()

    if translated_list:
        with open(f"{_word}.txt", 'a+') as file:
            print(f"\n{_out_language.capitalize()} Translation:", file=file)
            print(*translated_list, sep="\n", file=file)
            print(f"\n{_out_language.capitalize()} Examples:", file=file)
            print(*examples, sep='\n', file=file)


supported_languages = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                       'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')


def main():
    if len(sys.argv) != 4:
        exit(print("Fatal error. 4 arguments required."))

    input_language, output_language, word =\
        sys.argv[1], sys.argv[2], sys.argv[3].lower()

    if not exists(f"{word}.txt"):
        if output_language != "all":
            translate_to_file(input_language, output_language, word)
        else:
            for out_language in supported_languages:
                translate_to_file(input_language, out_language, word)

    with open(f"{word}.txt", 'r') as translations:
        print(translations.read())


if __name__ == "__main__":
    main()
