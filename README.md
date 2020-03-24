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
