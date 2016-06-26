#!/usr/bin/env python -tt

import sys


def make_cols(mood, tense):
    return "{}\t{}".format(mood, tense)


conv_key = {"g0":  make_cols("gerund",     "gerund"),
            "ic": make_cols("indicative",  "conditional"),
            "if": make_cols("indicative",  "future"),
            "ii": make_cols("indicative",  "imperfect"),
            "ip": make_cols("indicative",  "present"),
            "is": make_cols("indicative",  "preterite"),
            "m0" : make_cols("imperative", "imperative"),
            "n0" : make_cols("infinitive", "infinitive"),
            "p0" : make_cols("participle", "participle"),
            "si": make_cols("subjunctive", "imperfect"),
            "sp": make_cols("subjunctive", "present"),
            "sf": make_cols("subjunctive", "future")}



for line in sys.stdin:
    try:
        line = line.rstrip()[::-1].lower()
        tag, verb = map(lambda x: x[::-1], line.split("_", 1))
        tag = tag[2:-3]
        print("{}\t{}".format(verb, conv_key[tag]))
    except:
        pass

