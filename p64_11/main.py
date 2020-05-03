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
        # 该状态id
        self.id = id
        # 该状态指向其它状态的边（二元组，形式为[终点，边名]）
        self.to = []
        # 标志是否是起点/终点
        self.isStart = False
        self.isEnd = False
        # 遍历时的标记变量
        self.isVisited = False

    def nodeId(self):
        # 返回该状态id
        return self.id

    def pointTo(self, to, edge):
        # 将边的二元组添加到self.to中
        self.to.append([to, edge])

    def getDst(self, edge):
        # 通过边名得到终点list
        result = []
        for item in self.to:
            if item[1] == edge:
                result.append(item[0])
        return result

    def toStr(self):
        # 打印所有以该状态为起点的边
        if self.to:
            for item in self.to:
                print('[{}]==[{}]=>[{}]'.format(
                    self.id, item[1], item[0].nodeId()))

    def draw(self, pic):
        # 使用Graphviz绘图
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
        # list存储所有状态节点
        self.list = []
        # id用来依次给状态编号
        self.id = id()

    def getNode(self, index=-1):
        # 获取指定位置的状态节点
        try:
            return self.list[index]
        except IndexError:
            print('错误：数组越界')

    def newNode(self):
        # 添加新状态节点
        self.list.append(node(self.id.getId()))
        return self.getNode()

    def getResult(self):
        # 打印所有边
        for item in self.list:
            item.toStr()

    def clearHistory(self):
        # 清空遍历历史
        for item in self.list:
            item.isVisited = False

    def drawPic(self, pic):
        # 绘制状态图
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
    print('-----------------')
    print('NFA连接情况')
    nodes.getResult()
    print('-----------------')
    # 绘制NFA
    nodes.drawPic(NFA)


def toDFA():
    # NFA确定化为的DFA
    DFA = Digraph('DFA', comment="DFA", format="png")
    DFA.graph_attr['rankdir'] = 'LR'
    originNodes = nodeList()
    alphabet = []
    count = int(input('请输入状态数量(编号为0，1，2，...)：'))
    for _ in range(count):
        originNodes.newNode()
    print('请输入起点编号：')
    startIndex = int(input())
    originNodes.getNode(startIndex).isStart = True
    print('请输入终点编号：')
    endIndex = int(input())
    originNodes.getNode(endIndex).isEnd = True

    print('请输入边信息（格式为“起点编号 终点编号 边名”，以-1结束）：')
    while (True):
        tmp = input().split(' ')
        start = int(tmp[0])
        if start != -1:
            end = int(tmp[1])
            edge = tmp[2]
            originNodes.getNode(start).pointTo(originNodes.getNode(end), edge)
            alphabet.append(edge)
        else:
            break
    # 字母表去重
    alphabet = list(set(alphabet))
    # 删掉字母表中的ε
    alphabet.remove('ε')
    # 构造空闭环列表
    closure = []
    for item in originNodes.list:
        dst = item.getDst('ε')
        stack = list(dst)
        dst.append(item)
        for node in stack:
            node.isVisited = True
        while stack:
            tmp = stack.pop().getDst('ε')
            dst = dst+tmp
            for node in tmp:
                if not node.isVisited:
                    stack.append(node)
                    node.isVisited = True
        closure.append(list(set(dst)))
        originNodes.clearHistory()
    # 标记起点的空闭环
    start = closure[startIndex]
    # 初始化新的状态节点列表（重新构造图）
    newNodes = nodeList()
    newNodes.newNode()
    newNodes.getNode().isStart = True
    # tmpNodes存储新节点，stack作为栈使用
    tmpNodes = [start]
    stack = [start]
    while stack:
        # 从栈中弹出一个状态集
        tmp = stack.pop()
        # 记录该集合对应的状态节点列表中的节点
        startNode = newNodes.getNode(tmpNodes.index(tmp))
        # 遍历字母表中的所有内容
        for letter in alphabet:
            dst = []
            # 遍历状态集中的所有状态，记录他们跳转到的节点，存入到dst中
            for node in tmp:
                dst += node.getDst(letter)
            # 对dst去重（此时的dst保存的是跳转到的状态）
            dst = list(set(dst))
            result = []
            for node in dst:
                # 得到该节点的编号
                index = originNodes.list.index(node)
                # 获取对应编号的空闭环
                result += closure[index]
            # 对result去重
            result = list(set(result))
            if result not in tmpNodes:
                # 对新状态编号，保存，入栈，进行相应指向
                tmpNodes.append(result)
                stack.append(result)
                newNodes.newNode()
                startNode.pointTo(newNodes.getNode(), letter)
                # 如果状态集中有原来的终点，则该状态集同样作为终点
                if originNodes.getNode(endIndex) in result:
                    newNodes.getNode().isEnd = True
            else:
                # 否则仅进行相应指向
                startNode.pointTo(newNodes.getNode(
                    tmpNodes.index(result)), letter)
    # 构造DFA结束，打印结果
    print('-----------------')
    print('DFA连接情况')
    newNodes.getResult()
    print('-----------------')
    # 绘制DFA
    newNodes.drawPic(DFA)


def toMinDFA():
    print('待实现')


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
