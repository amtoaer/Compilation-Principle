# 实验二

## 题目

表达式语法分析器的设计。

## 要求

![image-20200606142213354](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200606142213354.png)

## 思路

从设计要求来分析，最终只需要输出表达式是否正确，故只需简单实现一个判断类别的词法分析器。

需要识别出来的类别有六个，其中`I`为数字或常量，相当于实验一中的数字/变量名，另外五个分别为`ω0`、`ω1`、`(`、`)`和`#`，简单进行单字符识别便可实现。

对词法分析器进行封装，暴露`getToken()`方法，每次调用读入一个`token`并返回结果。

词法分析器的实现上，（为了简单）我选用了递归下降子程序法和LL(1)分析法，引用词法分析器作为`self.analyzer`，`w`同样作为类内变量，封装一个相当于`next(w)`的方法：

```python
def next(self):
    self.w = self.analyzer.getToken()
```

接着只需要画出递归子程序/LL(1)分析表，按照一般方法实现逻辑即可完成任务。

