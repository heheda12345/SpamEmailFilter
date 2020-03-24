import json
import re
import random
import sys
from collections import Counter
from math import log

DEBUG = 0

def load():
    global items
    items = json.load(open('../log/raw.dump'))[:-1]
    random.seed(0)
    random.shuffle(items)

def run(args):
    foldSize = 6480
    folds = []
    for i in range(5):
        train = items[: foldSize * i] + items[foldSize * (i + 1): ]
        test = items[foldSize * i: foldSize * (i + 1)]
        init(train, args)
        fold = []
        spam = 0
        noSpam = 0
        for item in test:
            if select(item):
                fold.append(item)
                if item['spam']:
                    spam += 1
                else:
                    noSpam += 1
        print("fold {}: spam {} nospam {}".format(i, spam, noSpam))
        folds.append(fold)
    json.dump(folds, open("../log/test.dump", "w"))

def isBase64(st):
    st = st.strip()
    regex = re.compile(r"[a-zA-Z0-9\+/\n=]+", re.S)
    return len(st) > 20 and len(st.split(" ")) == 1 and re.fullmatch(regex, st) is not None

def BMinus(st):
    return re.search('B---------------------', st) is not None

def split(st):
    words = re.findall("[a-zA-Z\-\.'/@:]+", st)
    for j, word in enumerate(words):
        if (word[-1] == '.'):
            word = word[:-1]
        words[j] = word
    return words

def confirmSpam(item):
    return isBase64(item['content']) or BMinus(item['content'])

def init(items, args):
    spamWords = []
    noSpamWords = []

    for (i, item) in enumerate(items):
        if confirmSpam(item):
            continue        
        words = split(item['content'])
        if item['spam']:
            spamWords += words
        else:
            noSpamWords += words

    spamWords = Counter(spamWords)
    noSpamWords = Counter(noSpamWords)

    global wordList
    wordList = {}
    for i, x in enumerate(spamWords):
        wordList[x] = [spamWords[x], noSpamWords[x]]

    for i, x in enumerate(noSpamWords):
        wordList[x] = [spamWords[x], noSpamWords[x]]

def select(item):
    if confirmSpam(item):
        return False

    words = split(item['content'])
    zeroSpam = 0
    zeroNoSpam = 0
    for word in words:
        if word not in wordList:
            continue
        x = wordList[word]
        if x[0] == 0:
            zeroSpam += x[1]
            continue
        if x[1] == 0:
            zeroNoSpam += x[0]
            continue
    return (zeroNoSpam > 0 and zeroSpam > 0) or (zeroNoSpam == 0 and zeroSpam == 0)

if __name__ == '__main__':
    load()
    run({})
