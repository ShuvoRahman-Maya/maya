import re
from html.parser import HTMLParser
from html import unescape
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MyHTMLParser(HTMLParser):
    string = ''

    def handle_data(self, data):
        # \u200c zero width non zoiner
        self.string += data.replace('\u200c','')


class Preprocessor:
    bangla_numbers = ['০','১','২','৩','৪','৫','৬','৭','৮','৯']
    english_numbers = ['0','1','2','3','4','5','6','7','8','9']

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


class LanguageSeparator:
    pass


if __name__ == '__main__':
    from database_connection import DatabaseConnection
    db_conn = DatabaseConnection()
    connection = db_conn.connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id,body,source from questions_raw where id=6778"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                if i['source'] != 'app':
                    a = i['body'].encode('latin').decode('utf-8')
                    a = Preprocessor.punctuation_remover(a)
                else:
                    decoded_data = unescape(i['body'])
                    parser = MyHTMLParser()
                    parser.feed(decoded_data)
                    a = Preprocessor.punctuation_remover(parser.string)
                pre = Preprocessor()
                # lang = LanguageSeparation()
                a = Preprocessor.remove_extra_whitespace(a)
            print(a)
    finally:
        connection.close()