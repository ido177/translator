import requests
from bs4 import BeautifulSoup
import argparse
import sys


class UnsupportedLanguage(Exception):
    def __init__(self, language):
        print(f"Sorry, the program doesn't support {language}")
        super().__init__()
        sys.exit()


class Disconnect(Exception):
    def __init__(self):
        print('Something wrong with your internet connection')
        super().__init__()
        sys.exit()


class UnableToFind(Exception):
    def __init__(self, word):
        print(f"Sorry, unable to find {word}")
        super().__init__()
        sys.exit()


class Translator:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('translate_from')
        self.parser.add_argument('translate_to')
        self.parser.add_argument('word')
        self.args = self.parser.parse_args()
        self.lang_from = self.args.translate_from.capitalize()
        self.word = self.args.word
        lang_to = self.args.translate_to.capitalize()
        ind_from = languages.index(self.lang_from)

        if lang_to not in languages and lang_to != 'All':
            raise UnsupportedLanguage(lang_to)
        if self.lang_from not in languages and self.lang_from != 'All':
            raise UnsupportedLanguage(lang_to)

        with CmFile(self.word) as self.file:
            if lang_to == 'All':
                for lang in languages:
                    if lang != languages[ind_from]:
                        self.con(lang)
            else:
                self.con(lang_to)

    def con(self, lang_to):
        link = f'https://context.reverso.net/translation/{self.lang_from.lower()}-{lang_to.lower()}/{self.word}'
        r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        if not r.status_code:
            raise Disconnect
        soup = BeautifulSoup(r.content, 'html.parser')
        self.translations(soup, lang_to)

    def translations(self, soup, lang_to):
        translated = []
        examples = []
        for item in soup.find_all('a', class_='translation'):
            translated.append(item.text.strip())
        if len(translated) < 1:
            raise UnableToFind(self.word)
        for item in soup.find_all('div', {'class': ['src', 'trg']}):
            examples.append(item.text.strip())
        examples = list(filter(None, examples))
        self.console_output(translated, examples, lang_to)
        self.file_output(translated, examples, lang_to)

    def console_output(self, translated, examples, lang_to):
        print(f'\n{lang_to} Translations:')
        print(translated[0])
        print(f'\n{lang_to} Examples:')
        print(f'{examples[0]}\n{examples[1]}')

    def file_output(self, translated, examples, lang_to):
        self.file.write(f'{lang_to} Translations:\n')
        self.file.write(f'{translated[0]}\n\n')
        self.file.write(f'{lang_to} Examples:\n')
        self.file.write(f'{examples[0]}\n')
        self.file.write(f'{examples[1]}\n\n')


class CmFile:
    def __init__(self, word):
        self.word = word

    def __enter__(self):
        self.file = open(f'{self.word}.txt', 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


languages = ['Arabic', 'German', 'English', 'Spanish',
             'French', 'Hebrew', 'Japanese', 'Dutch',
             'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

if __name__ == '__main__':
    Translator()
