#!/usr/bin/env python -tt

from collections import Counter
import unicodedata

words = []

with open("./all-verbs.txt", "rb") as fh:
    words = fh.readlines()

words = [unicodedata.normalize("NFC", item.decode("utf-8").rstrip()) for item in words]

cnt = Counter()
for word in words:
    cnt[word] += 1

for item in cnt.most_common(None):
    print("{}\t{}".format(item[1], item[0]))

