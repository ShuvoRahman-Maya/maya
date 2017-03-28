import re
from html.parser import HTMLParser
from html import unescape
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MyHTMLParser(HTMLParser):
    string = ''

    def handle_data(self, data):
        # \u200c zero width non zoiner
        self.string += data.replace('\u200c', '')


class Preprocessor:
    bangla_numbers = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
    english_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def replace_numbers(self, token_list):
        for index, item in enumerate(token_list):
            for i in self.bangla_numbers:
                if i in item:
                    token_list[index] = '__digit__bn__'
                    break
            for i in self.english_numbers:
                if i in item:
                    token_list[index] = '__digit__en__'
                    break

        return token_list

    @staticmethod
    def tokenize(text):
        return text.split(' ')

    @staticmethod
    def remove_extra_whitespace(text):
        return re.sub('\s+', ' ', text).strip()

    @staticmethod
    def convert_to_lowercase(text):
        return text.lower()

    @staticmethod
    def decode_text(text, type):
        # utf-8 decode
        if type == 1:
            return text.encode('latin').decode('utf-8')
        # html entity decode
        elif type == 2:
            parser = MyHTMLParser()
            parser.feed(unescape(text))
            return parser.string

    @staticmethod
    def punctuation_remover(data):
        import string
        try:
            remove_punctuation_map = dict((ord(char), u' ') for char in string.punctuation)
            for i in [2404, 55357, 56842, 55356, 57198, 57252, 128522]:
                remove_punctuation_map[i] = u' '
            return data.translate(remove_punctuation_map)
        except TypeError:
            return None


class LanguageSeparation:
    en_word_set = set()

    def __init__(self):
        with open('/Users/shuvo/Downloads/maya_article_en.txt', 'r') as file:
            english_text = file.read()
        english_text = english_text.split(' ')

        for word in english_text:
            self.en_word_set.add(word)

    def language_detection(self, text):
        # input text as a string
        # bangla = 0
        # english = 1
        # banglish = 2
        size = len(text)
        bn_count, en_count = 0, 0
        for letter in text:
            try:
                letter.encode('ascii')
            except UnicodeEncodeError:
                bn_count += 1
            except UnicodeError:
                bn_count += 1
            else:
                en_count += 1
        try:
            bn_prob = float(bn_count) / size
        except ZeroDivisionError:
            return 'bn'
        if bn_prob > 0.60:
            return 'bn'
        else:
            words = text.split(' ')
            no_words = len(words)
            en_word_count = 0
            for word in words:
                if word in self.en_word_set:
                    en_word_count += 1
            en_prob = float(en_word_count) / no_words
            if en_prob > 0.50:
                return 'en'
            else:
                return 'banglish'
