#!/usr/bin/env python -tt

###########################################################
##                                                       ##
##   combine.py                                          ##
##                                                       ##
##                Author: Tony Fischetti                 ##
##                        tony.fischetti@gmail.com       ##
##                                                       ##
###########################################################



import sys
import json
import unicodedata


SUPP = json.loads(open("./finished-supplemented.json", "rb").read().decode("utf-8"))


def main():
    with open("./all.txt", "rb") as fh:
        lines = [item.decode("utf-8").rstrip() for item in fh.readlines()]
    for line in lines:
        verb, mood, tense = line.split("\t")
        verb = unicodedata.normalize("NFC", verb)

        if mood == "infinitive":
            infinitive = verb
            print("{}\t{}\t{}\t{}".format(verb, infinitive, tense, mood))
            continue

        if verb not in SUPP:
            # print("the verb wasn't in the JSON :(")
            continue

        this_dict = SUPP[verb]
        if not this_dict["infinitive"]:
            # print("unable to find infinitive :(")
            continue
        infinitive = this_dict["infinitive"]
        infinitive = unicodedata.normalize("NFC", infinitive)
        # print("=> INFINITIVE: ->{}<-".format(infinitive))
        print("{}\t{}\t{}\t{}".format(verb, infinitive, tense, mood))





if __name__ == '__main__':
    STATUS = main()
    sys.exit(STATUS)

