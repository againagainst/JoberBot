import os.path
import sys
import random

import pymorphy2


def select(ifile, minlen=13):
    term_opath = os.path.join("data", "zdb_term_selected_utf8.txt")
    opath = os.path.join("data", "zdb_selected_utf8.txt")
    odata, term_odata = list(), list()
    morph = pymorphy2.MorphAnalyzer()
    with open(ifile, "r") as ifp:
        for line in ifp:
            word = line.strip()
            if len(word) < minlen:
                continue
            if word.endswith('изм') or word.endswith('ость'):
                term_odata.append(word)
            try:
                parsed = morph.parse(word)[0]
            except Exception as e:
                print(word, "—", e)
                continue
            if not parsed.tag.POS == "NOUN":
                continue
            odata.append(word)

    random.shuffle(term_odata)
    random.shuffle(odata)
    with open(term_opath, "w") as ofp:
        ofp.write("\n".join(term_odata))
    with open(opath, "w") as ofp:
        ofp.write("\n".join(odata))


if __name__ == "__main__":
    select(sys.argv[1])
