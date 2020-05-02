#!/usr/bin/python
try:
    from graphviz import Digraph
except:
    print('缺少graphviz包，无法运行')


class id():
    # id自增器(用于给状态编号)
    def __init__(self, id=-1):
        self.id = id

    def getId(self):
        self.id += 1
        return self.id


class node():
    # 状态节点类
    def __init__(self, id):
        self.id = id
        self.to = []
        self.isStart = False
        self.isEnd = False
        self.isVisited = False

    def nodeId(self):
        return self.id

    def pointTo(self, to, edge):
        self.to.append([to, edge])

    def toStr(self):
        if self.to:
            for item in self.to:
                print('[{}]==[{}]=>[{}]'.format(
                    self.id, item[1], item[0].nodeId()))

    def draw(self, pic):
        # 绘制点
        label = str(self.id)
        if self.isStart:
            label += '+'
        if self.isEnd:
            label += '-'
        pic.node(str(self.id), label)
        # 绘制边
        if self.to:
            for item in self.to:
                pic.edge(str(self.id), str(
                    item[0].nodeId()), label=item[1])


class nodeList():
    # 封装状态节点数组
    def __init__(self):
        self.list = []
        self.id = id()

    def getNode(self, index=-1):
        try:
            return self.list[index]
        except IndexError:
            print('错误：数组越界')

    def newNode(self):
        self.list.append(node(self.id.getId()))
        return self.getNode()

    def getResult(self):
        for item in self.list:
            item.toStr()

    def drawPic(self, pic):
        # 全部绘制并展示
        for item in self.list:
            item.draw(pic)
        try:
            pic.view()
        except:
            print('缺少graphviz可执行程序，图片无法显示')


def toNFA():
    # 正规式生成的NFA
    NFA = Digraph('NFA', comment="NFA", format="png")
    NFA.graph_attr['rankdir'] = 'LR'
    # 输入
    str = input('请输入正规式（未处理非法输入）：')
    nodes = nodeList()
    # 用于保存状态历史
    starts = []
    # 括号子问题的终点栈
    ends = []
    # 括号子问题的起点栈
    flag = []
    # 初始化，分配起始状态
    starts.append(nodes.newNode())
    starts[-1].isStart = True
    i = 0
    while i < len(str):
        if str[i] == '(':
            # 增加终点便于处理括号里有或的情况，保存起点便于或、闭包的回溯
            ends.append(nodes.newNode())
            flag.append(starts[-1])
        elif str[i] == '*':
            if (str[i - 1]) == ')':
                # 如果前面有括号，则将当前状态和括号前的状态用双向ε边连接，该操作后括号前状态的位置失去作用，应该弹出
                starts[-1].pointTo(flag[-1], 'ε')
                flag[-1].pointTo(starts[-1], 'ε')
                flag.pop()
            else:
                # 否则将当前状态和上一个状态用双向ε边连接
                starts[-1].pointTo(starts[-2], 'ε')
                starts[-2].pointTo(starts[-1], 'ε')
        elif str[i] == ')':
            # 将当前所处位置和终点连接起来，令当前点等于终点
            starts[-1].pointTo(ends[-1], 'ε')
            starts.append(ends.pop())
        elif str[i] == '|':
            # 将当前所处位置和终点连接起来，令当前点等于起点
            starts[-1].pointTo(ends[-1], 'ε')
            starts.append(flag[-1])
        else:
            # 普通情况，只需分配新状态，然后将两状态相连
            starts.append(nodes.newNode())
            starts[-2].pointTo(starts[-1], str[i])
        i = i + 1
    starts[-1].isEnd = True
    print('NFA连接情况')
    nodes.getResult()
    print('-----------------')
    # 绘制NFA
    nodes.drawPic(NFA)


def toMinDFA():
    pass


def toDFA():
    # NFA确定化为的DFA
    DFA = Digraph('DFA', comment="DFA", format="png")
    DFA.graph_attr['rankdir'] = 'LR'
    originNodes = nodeList()
    alphabet = []
    count = int(input('请输入状态数量(编号为0，1，2，...)：'))
    for _ in range(count):
        originNodes.newNode()
    print('请输入起点编号（以-1结束）：')
    while (True):
        tmp = int(input())
        if tmp != -1:
            originNodes.getNode(tmp).isStart = True
        else:
            break
    print('请输入终点编号（以-1结束）：')
    while (True):
        tmp = int(input())
        if tmp != -1:
            originNodes.getNode(tmp).isEnd = True
        else:
            break
    print('请输入边信息（格式为“起点编号 终点编号 边名”，以-1结束）：')
    while (True):
        start = int(input())
        if start != -1:
            end = int(input())
            edge = input()
            originNodes.getNode(start).pointTo(originNodes.getNode(end), edge)
            alphabet.append(edge)
        else:
            break
    # 字母表去重
    alphabet = list(set(alphabet))
    # 单设节点组用于存储DFA状态信息
    # 一集合用于保存所有出现过的状态集，另一集合用作栈
    DFANodes = nodeList()
    DFASet = []
    tempStack = []
    # 构建起点集
    begin = []
    # 该变量用于标记起点中是否含有终点
    isEnd = False
    for node in originNodes.list:
        if node.isStart:
            begin.append(node)
            isEnd = isEnd or node.isEnd
    # 将起点加入双列表
    DFASet.append(begin)
    tempStack.append(begin)
    # 新状态节点作为起始状态
    temp = DFANodes.newNode()
    temp.isStart = True
    temp.isEnd = isEnd
    while tempStack:
        start = tempStack.pop()
        for letter in alphabet:
            result = []
            # 得到当前处理的起点角标
            startIndex = DFASet.index(start)
            for node in start:
                result += node.getEnd(letter)
            # 对result进行去重，得到跳转结果
            result = list(set(result))
            # 如果状态集未出现过且不为空，则将其压栈，加入出现过的状态集，取对应节点，插入边
            if result:
                if result not in DFASet:
                    DFASet.append(result)
                    tempStack.append(result)
                    tmp = DFANodes.newNode()
                    DFANodes.getNode(startIndex).pointTo(
                        tmp, letter)
                    isEnd = False
                    isStart = False
                    for node in result:
                        isEnd = isEnd or node.isEnd
                        isStart = isStart or node.isStart
                    tmp.isStart = isStart
                    tmp.isEnd = isEnd
                else:
                    DFANodes.getNode(startIndex).pointTo(
                        DFANodes.getNode(DFASet.index(result)), letter)
    # 操作完成，打印结果
    print('DFA连接情况')
    DFANodes.getResult()
    # 画图
    DFANodes.drawPic(DFA)


def main():
    print('''欢迎使用，请选择功能：
    1. 正规式转NFA
    2. NFA确定化
    3. NFA最小化''')
    choice = int(input())
    if choice == 1:
        toNFA()
    elif choice == 2:
        toDFA()
    elif choice == 3:
        toMinDFA()
    else:
        print('选择错误，正在退出...')


if __name__ == '__main__':
    main()
