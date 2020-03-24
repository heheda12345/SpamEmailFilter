# SpamEmailFilter
Project of Introduction to Machine Learning, Tsinghua University, 2020 spring; A simple spam email filter base on Naïve Bayes Classifier on 
## 数据集
选python可以直接解码的文件，共32401/37822，取其中32400个（为了能整除，但不做也行, shuffle, 6480 test set

分词，把句号去掉



概率为0：直接确定是什么，而不是做平滑

https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt

## 实验结果
accuracy/precision/recall
naive: 0.9724/0.9945/0.9607 特判base64和BMinus，剩下的直接词频统计（>10有效）
wordlist: naive基础上，仅考虑在20000词表里出现的单词，内有参数lower表示是否归一为小写
    nolower: 0.9404/0.9954/0.9078/0.9496
    lower: 0.8833/0.9949/0.8157/0.8962
    nolower 再加上 spam里的非词表内容 0.9718/0.9923/0.9619/0.9769
    nolower 再加上非spam里的非词表内容 0.9467/0.9962/0.9174/0.9552