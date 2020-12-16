import codecs
import operator
import os
import time
import matplotlib
import io
from PIL import Image
import matplotlib.pyplot as plt

matplotlib.use('agg')


class FileInfo:
    def __init__(self, file_path, car_str, enc="utf-8"):
        self.file_path = file_path
        self.enc = enc
        self.car_str = car_str

    @property
    def text(self):
        with codecs.open(self.file_path, encoding=self.enc, errors="ignore") as file:
            return file.read().lower()

    def count_words(self, word_dict=None):
        if word_dict is None:
            word_dict = {}

        word = ""
        for i in self.text:
            if i in self.car_str:
                if i != " ":
                    word += i
                else:
                    if word != "":
                        if word in word_dict:
                            word_dict[word] += 1
                        else:
                            word_dict[word] = 1
                        word = ""
        return word_dict


class FilesInfo:
    def __init__(self, folder="books/", lang=0):

        en = ("en", "english", "abcdefghijklmnopqrstuvwxyz ")
        ru = ("ru", "russian", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
        ua = ("ua", "ukranian", "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя ")
        nu = ("nu", "numbers", "1234567890 ")

        self.langs = [en, ru, ua, nu]
        self.langs.insert(0, self.all_lang)
        self.car_str = self.langs[lang][2]
        self.folder = folder

    @property
    def all_lang(self):
        lang_s = " "
        for lang in self.langs:
            for s in lang[2].replace(" ", ""):
                lang_s += s
        return "al", "all languages", lang_s

    @property
    def av_paths(self):
        files = []
        for filename in os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}/{self.folder}"):
            if filename.endswith(".txt"):
                files.append(f"{self.folder}{filename}")
        return files

    @staticmethod
    def sort_dict(word_dict):
        return sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)

    def count_words(self):
        start = time.perf_counter()
        word_dict = {}
        for file_path in self.av_paths:
            file_info = FileInfo(file_path, self.car_str)
            word_dict = file_info.count_words(word_dict)
            print(file_path)
        print(f"It took {round(time.perf_counter() - start, 3)} second(s)!")
        return self.sort_dict(word_dict)

    @staticmethod
    def plot(lst, words=100):
        lst1 = list(list(zip(*lst))[0])
        lst2 = list(list(zip(*lst))[1])

        if len(lst) > words:
            plt.plot(lst1[:words], lst2[:words])
        else:
            plt.plot(lst1, lst2)
        buf = io.BytesIO()
        plt.savefig(buf, lang=1, format='png', dpi=900)
        buf.seek(0)
        im = Image.open(buf)
        im.show()
        buf.close()


if __name__ == '__main__':
    a = FilesInfo(folder="books/", lang=1)
    a.plot(a.count_words())
