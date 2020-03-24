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

def average(x):
    return sum(x)/len(x)

def testAll(args):
    foldSize = 6480
    tp = []
    tn = []
    fp = []
    fn = []
    for i in range(5):
        train = items[: foldSize * i] + items[foldSize * (i + 1): ]
        test = items[foldSize * i: foldSize * (i + 1)]
        init(train, args)
        TP = TN = FP = FN = 0
        for item in test:
            if ignore(item):
                continue
            ans = testOne(item, args)
            if ans and item['spam']:
                TP += 1
            elif ans and not item['spam']:
                FP += 1
            elif not ans and item['spam']:
                FN += 1
            elif not ans and not item['spam']:
                TN += 1
        tp.append(TP)
        fp.append(FP)
        fn.append(FN)
        tn.append(TN)
        if DEBUG:
            break

    acc = [(TP + TN) / (TP + TN + FP + FN) for TP, TN, FP, FN in zip(tp, tn, fp, fn)]
    precision = [TP / (TP + FP) for TP, FP in zip(tp, fp)]
    recall = [TP / (TP + FN) for TP, FN in zip(tp, fn)]
    f1 = [2 * p * r / (p + r) for p, r in zip(precision, recall)]
    return {
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn,
        'acc': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def printOne(result):
    print("")
    print("\033[1;34m Approach: {}\033[0m".format(sys.argv[0]))
    print("\033[1;32m True positive: {}\033[0m {}".format(average(result['tp']), result['tp']))
    print("\033[1;32m True negetive: {}\033[0m {}".format(average(result['tn']), result['tn']))
    print("\033[1;32m False positive: {}\033[0m {}".format(average(result['fp']), result['fp']))
    print("\033[1;32m False negetive: {}\033[0m {}".format(average(result['fn']), result['fn']))
    print("\033[1;35m Accuracy: {}\033[0m {}".format(average(result['acc']), result['acc']))
    print("\033[1;35m Precision: {}\033[0m {}".format(average(result['precision']), result['precision']))
    print("\033[1;35m Recall: {}\033[0m {}".format(average(result['recall']), result['recall']))
    print("\033[1;35m F1: {}\033[0m {}".format(average(result['f1']), result['f1']))
        

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

def ignore(item):
    return confirmSpam(item) or not isSingle(item)

def init(items, args):
    global spamTotal
    global noSpamTotal
    spamTotal = noSpamTotal = 0
    for (i, item) in enumerate(items):
        if confirmSpam(item):
            continue
        if (item['spam']):
            spamTotal += 1
        else:
            noSpamTotal += 1

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

def isSingle(item):
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
    if zeroSpam > 0 or zeroNoSpam > 0:
        return True
    return False

def testOne(item, args):
    if (confirmSpam(item)):
        return True
    words = split(item['content'])
    sumSpam = 0.0
    sumNoSpam = 0.0
    zeroSpam = 0
    zeroNoSpam = 0
    for word in words:
        if word not in wordList:
            continue
        x = wordList[word]
        if x[0] == 0:
            zeroSpam += x[1]
            # print(word, item['path'], x)
            continue
        if x[1] == 0:
            zeroNoSpam += x[0]
            # print(word, item['path'], x)
            continue
        sumSpam += log(x[0] * 1.0 / spamTotal)
        sumNoSpam += log(x[1] * 1.0 / noSpamTotal)
    if zeroSpam > 0 or zeroNoSpam > 0:
        return zeroSpam < zeroNoSpam
    assert(False)
    return sumSpam - log(spamTotal) > sumNoSpam - log(noSpamTotal)

if __name__ == '__main__':
    load()
    result = testAll({})
    printOne(result)
