<h1 align="center">编译原理第一次作业</h1>

## 题目

### P63

+   编写一个对于`Pascal`源程序的预处理程序。该程序的作用是，每次被调用时都将下一个完整的语句送进扫描缓冲区，去掉注解行，同时要对源程序列表打印。

+   用类似`C`或`Pascal`的语言编写过程`GetChar`，`GetBC`和`Concat`。

+   用某种高级语言编写并调试一个完整的词法分析器。

### P64

+   用某种高级语言写出：

	1.  将正规式变成`NFA`的算法；
	2.  将`NFA`确定化的算法；
	3.  `DFA`状态最少化的算法。

## 进度

### P63

+   感觉题目描述不是很清楚，参考了[克总的实现](https://github.com/Rilliane/Compilers_Principles_Homework)。主要完成了去除三类单行注释后打印的任务。因为使用了`readline`进行逐行处理，暂不支持多行注释。

+   参照定义，实现较为轻松。

    +   `GetChar()`:读入下一个输入字符到ch中
    +   `GetBC()`:检查输入字符是否为空格，如果是空格则调用`GetChar()`直至非空
    +   `Concat()`:将ch中的字符连接到`strToken`之后

+   大概写了写，目前还有很多缺陷，比如只支持整型，界符/运算符写在一起等。待完善。

    >   5.5:修改了输出格式，便于截图

### P64

+   正规式转`NFA`，`NFA`转`DFA`已完成，`DFA`状态最少化基本完工。（忘记写去除无用状态了qaq）

    >   5.5:既然只交截图的话，是不是找个没有无用状态的例子就好，没必要再补去除无用状态了？
    >
    >   果然还是不补了！（滑稽）

## 截图

### P63

+   去掉了`Pascal`代码中的注释。

    ![深度截图_选择区域_20200504001414](https://i.loli.net/2020/05/04/qfYZD3BI7aGQO8b.png)

+   ![深度截图_选择区域_20200506112205](https://i.loli.net/2020/05/06/NXRB4p3nEjIrfmZ.png)

+   类型码编号规则写在了注释里

    ![深度截图_选择区域_20200505202947](https://i.loli.net/2020/05/05/9AE26vXIoVO4dfD.png)

### P64

+   +   正规式转`NFA`

        ![深度截图_选择区域_20200504001645](https://i.loli.net/2020/05/04/L8BgR5pJf3HjaAd.png)

    +   `NFA`转`DFA`

        >   测试样例选自[这篇文章](https://blog.csdn.net/u012359618/article/details/42456771).
        >
        >   测试`NFA`为：
        >
        >   ![20150106120049890](https://i.loli.net/2020/05/04/dfDVjBeLkHSQWxY.jpg)
        >
        >   标准结果为：
        >
        >   ![20150106200611099](https://i.loli.net/2020/05/04/a4TsxNzJQdntlMZ.jpg)

        ![深度截图_选择区域_20200504001930](https://i.loli.net/2020/05/04/hFHTK6qzwMnfNmu.png)
        
    +   `DFA`最小化
    
        >   测试样例选自[这篇文章](https://zhuanlan.zhihu.com/p/37900383).
        >
        >   测试`DFA`为（S为起点，从左到右，从上到下编号）：
        >
        >   ![v2-061cc56f74ff217c60e04da44d03cbaa_720w](https://i.loli.net/2020/05/04/mODqdcMnC1fiPyt.jpg)
        >
        >   标准结果为：
        >
        >   ![v2-9cdbf7afbe6227ae1e0eb36d880e7573_720w](https://i.loli.net/2020/05/04/NfQt3IajVvRHnCJ.jpg)

        ![深度截图_选择区域_20200504182248](https://i.loli.net/2020/05/04/V2r7zFOie6CXcwW.png)