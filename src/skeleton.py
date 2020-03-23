import json
import re
import random
import sys

def load():
    global items
    items = json.load(open('../log/raw.dump'))[:-1]
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
            elif not ans and item['spam']:
                FN += 1
            elif not ans and not item['spam']:
                TN += 1
        tp.append(TP)
        fp.append(FP)
        fn.append(FN)
        tn.append(TN)

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
        
def init(items, args):
    pass

def testOne(item, args):
    return True

if __name__ == '__main__':
    load()
    result = testAll({})
    printOne(result)
