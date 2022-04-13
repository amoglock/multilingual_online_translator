import requests
from bs4 import BeautifulSoup
import argparse

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
             'Portuguese', 'Romanian', 'Russian', 'Turkish']
headers = {'User-Agent': 'Mozilla/5.0'}
parser = argparse.ArgumentParser()
parser.add_argument('source_language')
parser.add_argument('target_language')
parser.add_argument('word')
args = parser.parse_args()


class Translator:
    soup = None

    def __init__(self, source_language, target_language, word, ):
        self.language = source_language
        self.target = target_language
        self.word = word
        self.get_page()

    def get_page(self):
        try:
            assert self.target.capitalize() in languages, f'Sorry, the program doesn\'t support {self.target}'
            page = requests.get(f'https://context.reverso.net/translation/{self.language}-{self.target}/{self.word}',
                                headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            assert page.status_code != 404, f'Sorry, unable to find {self.word}'
            assert page.status_code == 200, 'Something wrong with your internet connection'
            Translator.soup = soup
        except AssertionError as err:
            print(err)
            exit()


def translate_term(soup, language, limit=5):
    with open(f'{args.word}.txt', 'a', encoding='utf-8') as file:
        trans_tags = soup.find_all('a', {'class': 'translation'}, limit=limit + 1)
        term_list = list(map(lambda x: x.text.strip(), trans_tags))
        file.write(f'{language.capitalize()} {term_list[0]}:\n')
        for term in term_list[1:]:
            file.write(f'{term}\n')
        examples = soup.find_all('div', class_='src ltr', limit=limit)
        examples_list = list(map(lambda x: x.text.strip(), examples))
        translator_examples = soup.find_all('div', class_=['trg ltr', 'trg rtl arabic', 'trg rtl'], limit=limit)
        examples_translation = list(map(lambda y: y.text.strip(), translator_examples))
        file.write(f'\n{language.capitalize()} Example:\n')
        for i, j in zip(examples_list, examples_translation):
            file.write(f'{i}\n')
            file.write(f'{j}\n\n')
    print_file()


def print_file():
    with open(f'{args.word}.txt', 'r', encoding='utf-8') as file:
        print(file.read())


def main():
    if args.target_language == 'all':
        languages.remove(args.source_language.capitalize())
        for language_ in languages:
            Translator(args.source_language, language_.lower(), args.word)
            translate_term(Translator.soup, language=language_, limit=1)
    else:
        Translator(args.source_language, args.target_language, args.word)
        translate_term(Translator.soup, language=args.target_language)


if __name__ == '__main__':
    main()