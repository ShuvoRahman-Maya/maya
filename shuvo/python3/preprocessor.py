"""
[3:10]
you can then run a stemmer - like from TextBlob or Spacy

[3:11]
and tokenize the each row

[3:11]
so now each row is a list of tokenized words

"""
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
            for i in [2404, 55357, 56842, 55356, 57198, 57252]:
                remove_punctuation_map[i] = u' '
            return data.translate(remove_punctuation_map)
        except TypeError:
            return None


class LanguageSeparator:
    def

if __name__=='__main__':
    # texts = [
    #     "What is the 'male pillâ?",
    #     "Dear Maya Apa,  \n   Once during a class lecture, my lecturer mentioned that talcum powder can be harmful for our ovaries. My question is, is there any link between Talcum powder and ovarian diseases?\n",
    #     " অনেক ধন্যবাদ  \t Rota  virus সম্পর্কে বিস্তারিত   বলার জন্য। আমার বাচ্চার   বয়স এখন ২ মাস ২১ দিন তাহলে কি আমি কোন ভাবেই এখন এই টিকা দিতে পারবনা? RV5 যদি আমি ৪ মাস এবং ৬ মাসে দেয় তাহলে কি টিকা কাজ করবে ?"
    # ]
    # for i in texts:
    #     print(Preprocessor.remove_extra_whitespace(i))
    from database_connection import DatabaseConnection

    db_conn = DatabaseConnection()
    connection = db_conn.connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT body,source from questions where id>163100"
            cursor.execute(sql)
            result = cursor.fetchall()
        for i in result:
            if i['source']!='app':
                a= i['body'].encode('latin').decode('utf-8')
                a = Preprocessor.punctuation_remover(a)
            else:
                decoded_data = unescape(i['body'])
                parser = MyHTMLParser()
                parser.feed(decoded_data)
                a = Preprocessor.punctuation_remover(parser.string)
            pre = Preprocessor()
            # print(a)
            a = Preprocessor.tokenize(Preprocessor.remove_extra_whitespace(a))
            logging.info(pre.replace_numbers(a))

    finally:
        connection.close()
