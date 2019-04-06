import random
import sys

import pymorphy2


class SloganMaker:
    TERMS_FILE = "data/zdb_term_selected_utf8.txt"
    WORDS_FILE = "data/zdb_selected_utf8.txt"

    def __init__(self):
        with open(SloganMaker.WORDS_FILE, "r") as ifp:
            self.data = ifp.read().split("\n")

        with open(SloganMaker.TERMS_FILE, "r") as ifp:
            self.term_data = ifp.read().split("\n")

    def make_slogan(self):
        morph = pymorphy2.MorphAnalyzer()
        one = random.choice(self.term_data)
        two, three = random.sample(population=self.data, k=2)
        parsed = morph.parse(three)[0]
        three = parsed.inflect({"gent"}).word
        return "{0} — {1} {2}".format(one, two, three)


sloganmaker = SloganMaker()
