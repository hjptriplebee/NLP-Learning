# Byte Pair Encoding
相关论文[Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/pdf/1508.07909.pdf)

## 背景
许多NLP任务会根据语料生成一个字典，利用字典把词映射到向量空间。为了防止字典过大，通常需要设定词出现次数的阈值将出现次数较少的噪声词、生僻词剔除或编码成同一个字符。但这种方法有一个问题：如果测试时遇到了训练集中没有的词或因小于阈值而被剔除的词，那么对模型的性能会产生较大影响。

解决这个问题大致有两种方法：
1. 为低频词建立一个额外的表。这种方法只能处理低频词，仍然无法解决没有见过的词。
2. word-level encoding -> char-level encoding. 即不按照词进行编码，而是按照字进行编码。字是语言最基础的元素，因而所有词都可以用这种方法编码。但char-level模型的学习需要大量数据，这种方法在训练数据不足的情况下效果不好。

Byte Pair Encoding正是为了解决这些问题而提出。

## 算法流程
Byte Pair Encoding以无监督的方式从语料库里学习一种介于word-level和char-level之间的编码方式，这种编码方式以出现频词较高的字符串子串为基本元素。比如：learn、learning、learned，可能会被表示为learn、ing、ed的组合，即减少了词的数量，又避免了char-level难以表示语义信息的问题。过程如下：
1. 将词分成许多单个字符，并添加终止符；
2. 统计相邻字符串对出现的次数；
3. 获取出现次数最多的相邻字符串对；
4. 合并这个字符串对并替换上一轮字典中关于这两个字符串的表示；
5. 重复迭代直到达到设定次数。

代码[here](https://github.com/hjptriplebee/NLP-Learning/blob/master/BytePairEncoding/BytePairEncoding.py)

帮助理解的样例如下：
```
{'l o w #': 5, 'l o w e r #': 2, 'n e w e s t #': 6, 'w i d e s t #': 3}
best pairs: ('e', 's')
{'l o w #': 5, 'l o w e r #': 2, 'n e w es t #': 6, 'w i d es t #': 3}
best pairs: ('es', 't')
{'l o w #': 5, 'l o w e r #': 2, 'n e w est #': 6, 'w i d est #': 3}
best pairs: ('est', '#')
{'l o w #': 5, 'l o w e r #': 2, 'n e w est#': 6, 'w i d est#': 3}
best pairs: ('l', 'o')
{'lo w #': 5, 'lo w e r #': 2, 'n e w est#': 6, 'w i d est#': 3}
best pairs: ('lo', 'w')
{'low #': 5, 'low e r #': 2, 'n e w est#': 6, 'w i d est#': 3}
best pairs: ('n', 'e')
{'low #': 5, 'low e r #': 2, 'ne w est#': 6, 'w i d est#': 3}
best pairs: ('ne', 'w')
{'low #': 5, 'low e r #': 2, 'new est#': 6, 'w i d est#': 3}
best pairs: ('new', 'est#')
{'low #': 5, 'low e r #': 2, 'newest#': 6, 'w i d est#': 3}
best pairs: ('low', '#')
{'low#': 5, 'low e r #': 2, 'newest#': 6, 'w i d est#': 3}
best pairs: ('w', 'i')
{'low#': 5, 'low e r #': 2, 'newest#': 6, 'wi d est#': 3}
```

## Comment
1. 不适合中文，中文的编码已高度语义化，常用字较少。
2. 在cross-lingual的任务中目标语言与源语言都要使用BPE，以保证分割编码的一致性，但涉及中文时是否有效还有待实验。
