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
    global allTests
    allTests = json.load(open('../log/test.dump'))
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
            ans = testOne(item, args)
            if ans and item['spam']:
                TP += 1
            elif ans and not item['spam']:
                FP += 1
                # print("FP {}".format(item['path']))
            elif not ans and item['spam']:
                FN += 1
                # print("FN {}".format(item['path']))
            elif not ans and not item['spam']:
                TN += 1
        tp.append(TP)
        fp.append(FP)
        fn.append(FN)
        tn.append(TN)
        if DEBUG:
            break

    acc = [(TP + TN) / (TP + TN + FP + FN) for TP, TN, FP, FN in zip(tp, tn, fp, fn)]
    precision = [TP / max((TP + FP), 1) for TP, FP in zip(tp, fp)]
    recall = [TP / (TP + FN) for TP, FN in zip(tp, fn)]
    f1 = [2 * p * r / max(p + r, 1) for p, r in zip(precision, recall)]
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

def printOne(result, args):
    print("")
    print("\033[1;34m Approach: {} {}\033[0m".format(sys.argv[0], args))
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
    words = re.findall("[a-zA-Z0-9\-\.'/@:]+", st)
    for j, word in enumerate(words):
        if (word[-1] == '.'):
            word = word[:-1]
        words[j] = word
    return words

def confirmSpam(item):
    return isBase64(item['content']) or BMinus(item['content'])

def getTitle(item):
    x = re.search("(Subject|SUBJECT):(.*)", item['meta'])
    if x is not None:
        return x.group(2)
    x = re.search("(Subject|SUBJECT):(.*)", item['content'])
    return x.group(2) if x is not None else None

def confirmFilterNoSpam(item):
    return getTitle(item) is None

def getSender(item):
    x = re.search("From:.*?<(.*?@.*)>", item['meta'])
    if x is not None:
        return x.group(1)
    else:
        return None

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

    spamContent = []
    noSpamContent = []
    spamTitle = []
    noSpamTitle = []

    for (i, item) in enumerate(items):
        if confirmSpam(item):
            continue        
        words = split(item['content'])
        if item['spam']:
            spamContent += words
        else:
            noSpamContent += words

        title = getTitle(item)
        if title is not None:
            title = split(title)
            if item['spam']:
                spamTitle += title
            else:
                noSpamTitle += title
        
    spamContent = Counter(spamContent)
    noSpamContent = Counter(noSpamContent)
    spamTitle = Counter(spamTitle)
    noSpamTitle = Counter(noSpamTitle)

    global wordList
    wordList = {}
    for i, x in enumerate(spamContent):
        wordList[x] = [spamContent[x], noSpamContent[x], spamTitle[x], noSpamTitle[x]]
    for i, x in enumerate(noSpamContent):
        wordList[x] = [spamContent[x], noSpamContent[x], spamTitle[x], noSpamTitle[x]]
    for i, x in enumerate(spamTitle):
        wordList[x] = [spamContent[x], noSpamContent[x], spamTitle[x], noSpamTitle[x]]
    for i, x in enumerate(noSpamTitle):
        wordList[x] = [spamContent[x], noSpamContent[x], spamTitle[x], noSpamTitle[x]]

    spamSender = []
    noSpamSender = []
    for item in items:
        sender = getSender(item)
        if sender is None:
            continue
        # print(i, j, item['path'], item['spam'], mat)
        if (item['spam']):
            spamSender.append(sender)
        else:
            noSpamSender.append(sender)
    spamSender = Counter(spamSender)
    noSpamSender = Counter(noSpamSender)
    
    global senderList
    senderList = {}
    for x in spamSender:
        if (spamSender[x] + noSpamSender[x] > 10 and len(x) > 1):
            senderList[x] = [spamSender[x], noSpamSender[x]]
    for x in noSpamSender:
        if (spamSender[x] + noSpamSender[x] > 10 and len(x) > 1):
            senderList[x] = [spamSender[x], noSpamSender[x]]


def testOne(item, args):
    if (confirmSpam(item)):
        return True

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

    if zeroSpam == 0 and zeroNoSpam > 0:
        return True
    if zeroNoSpam == 0 and zeroSpam > 0:
        return False

    if (confirmFilterNoSpam(item)):
        return False
    
    sender = getSender(item)
    if sender in senderList:
        x = senderList[sender]
        if x[0] > 0 and x[1] == 0:
            return True
        if x[0] == 0 and x[1] > 0:
            return False

    FLAT = 0.01
    titleRate = 100

    sumSpam = 0.0
    sumNoSpam = 0.0

    words = split(item['content'])
    for word in words:
        if word not in wordList:
            continue
        x = wordList[word]
        freqSpam = x[0]
        freqNoSpam = x[1]
        if freqSpam == 0 or freqNoSpam == 0:
            sumSpam += log((freqSpam  + FLAT) * 1.0 / (spamTotal + FLAT * 2))
            sumNoSpam += log((freqNoSpam + FLAT) * 1.0 / (noSpamTotal + FLAT * 2))
        else:
            sumSpam += log(freqSpam * 1.0 / spamTotal)
            sumNoSpam += log(freqNoSpam * 1.0 / noSpamTotal)

    words = split(getTitle(item))
    for word in words:
        if word not in wordList:
            continue
        x = wordList[word]
        freqSpam = x[2]
        freqNoSpam = x[3] 
        if freqSpam == 0 or freqNoSpam == 0:
            sumSpam += log((freqSpam  + FLAT) * 1.0 / (spamTotal + FLAT * 2)) * titleRate
            sumNoSpam += log((freqNoSpam + FLAT) * 1.0 / (noSpamTotal + FLAT * 2)) * titleRate
        else:
            sumSpam += log(freqSpam * 1.0 / spamTotal) * titleRate
            sumNoSpam += log(freqNoSpam * 1.0 / noSpamTotal) * titleRate

    return sumSpam - log(spamTotal) > sumNoSpam - log(noSpamTotal)

if __name__ == '__main__':
    load()
    args = {}
    result = testAll(args)
    printOne(result, args)
