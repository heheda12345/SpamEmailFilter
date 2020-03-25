# 垃圾邮件识别
## 结果复现
1. 在根目录下新建`log/`文件夹，从https://cloud.tsinghua.edu.cn/d/2488ee6e8c694688b81d/ 下载两个文件，置于文件夹中
2. `cd src`
3. 使用命令`./run.sh final`复现最终结果，最终结果的代码位于`src/final.py`
3. 若想复现报告中的其他结果，可从报告的latex源码的相应表格的`\label{tab:文件名}`中获得文件名，并使用`./run.sh 文件名`运行。

## 最终结果
| Accuracy | Precision | Recall | F1 |
| - | -| - | - |
| 0.9918 | 0.9959 | 0.9908 | 0.9933 |

## 实验报告
见`doc/main.pdf`

## 联系方式
张晨，学号 2017011307，邮箱 zhangch99@outlook.com

