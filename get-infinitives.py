#!/usr/bin/env python -tt

###########################################################
##                                                       ##
##   get-infinitives.py                                  ##
##                                                       ##
##                Author: Tony Fischetti                 ##
##                        tony.fischetti@gmail.com       ##
##                                                       ##
###########################################################

"""

"""

__author__ = 'Tony Fischetti'
__version__ = '0.1'

import sys
import requests
import json
import re
import lxml.html
from lxml.cssselect import CSSSelector
import os
from lxml import etree
import html2text
import logging
import http.client as http_client
import urllib.parse
import time
import random
import unicodedata


PATTERN = re.compile("^\s*(\d+)\s+(.+?)$", re.UNICODE)
FN_VERB_LIST = "./all-verbs-count.txt"
VERB_LIST = []
# with open(FN_VERB_LIST, "r") as fh:
#     VERB_LIST = [item.rstrip() for item in fh.readlines()]
with open(FN_VERB_LIST, "rb") as fh:
    VERB_LIST = [item.decode("utf-8").rstrip() for item in fh.readlines()]
LENGTH = len(VERB_LIST)
TRANSLATE_STUB = "http://www.spanishdict.com/translate/"
BIG_DICT = {"verbs": {}}
MISMATCH_CSS = CSSSelector(".mismatch")

TEST1 = re.compile("represents different", re.UNICODE)
GET_INF1 = re.compile("\*\*.+?\*\* represents .+? \*\*(.+?)\*\*", re.UNICODE)

TEST2 = re.compile("\*\*.+?\*\* is the", re.UNICODE)
GET_INF2 = re.compile("\*\*.+?\*\* is the (\w+) form of \*\*(.+?)\*\* in the (\w+ \w+) (\w+)", re.UNICODE)

BK_REGEX = re.compile('<div variation-type="mismatch-verb.+?>(.+?)</div>',
                     re.UNICODE)


def parse_line(line):
    mat = PATTERN.search(line)
    return mat.group(1), mat.group(2)

def get_perc(ind):
    return round((float(ind+1)/LENGTH)*100, 2)


def main():
    for ind, line in enumerate(VERB_LIST):
        print("On {} of {} -> {}%".format(ind, LENGTH, get_perc(ind)))
        current_count, current_verb = parse_line(line)
        current_verb = unicodedata.normalize("NFC", current_verb)
        current_url = "{}{}".format(TRANSLATE_STUB, current_verb)
        print("Current verb: {}".format(current_verb))
        print("Current verb data: {}".format(current_verb.encode("utf-8")))
        print("Current count: {}".format(current_count))
        print("Current url: ->{}<-".format(current_url))

        try:
            r = requests.get(current_url)

            tree = lxml.html.fromstring(r.text)
            results = MISMATCH_CSS(tree)
            if results:
                print("# of matches: {}".format(len(results)))
            else:
                print("results is none")

            match = results[0]
            THE_TEXT = html2text.html2text(etree.tostring(match).decode("utf-8")).rstrip()

            the_infinitive = ""
            the_person = ""
            the_number = ""
            the_tense = ""
            AMB = False
            if TEST1.search(THE_TEXT):
                the_infinitive = GET_INF1.search(THE_TEXT).group(1)
                AMB = True
            elif TEST2.search(THE_TEXT):
                matches = GET_INF2.search(THE_TEXT)
                the_tense = matches.group(1)
                the_infinitive = matches.group(2)
                the_person = matches.group(3)
                the_number = matches.group(4)
                AMB = False
            print("The infinitive : >{}<".format(the_infinitive))

            if AMB:
                BIG_DICT[current_verb] = {"count": current_count,
                                          "spanish_dict_success": True,
                                          "infinitive": the_infinitive,
                                          "line": ind+1}
            else:
                BIG_DICT[current_verb] = {"count": current_count,
                                          "spanish_dict_success": True,
                                          "infinitive": the_infinitive,
                                          "line": ind+1}

        except:
            print("UNSPECIFIED FAILURE!")
            BIG_DICT[current_verb] = {"count": current_count,
                                      "spanish_dict_success": False,
                                      "infinitive": None,
                                      "line": ind+1}

        # with open("./mistakes/{}.html".format(current_verb), "w") as fh:
        #     fh.write(r.text)

        # every twenty
        if (ind % 20) == 0:
            out_str = json.dumps(BIG_DICT, sort_keys=True,
                                 indent=2, separators=(',', ': '))
            with open("./running.json", "w") as fh:
                fh.write(out_str)
        print()
        time.sleep(random.uniform(0.5, 2))

    out_str = json.dumps(BIG_DICT, sort_keys=True,
                         indent=2, separators=(',', ': '),
                         ensure_ascii=False)
    with open("./finished.json", "w") as fh:
        fh.write(out_str)





if __name__ == '__main__':
    STATUS = main()
    sys.exit(STATUS)

