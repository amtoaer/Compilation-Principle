#!/usr/bin/python
from lexical_analyzer import core


class recursive_descent():
    '''
    递归下降子程序分析法
    '''

    def __init__(self, line):
        self.analyzer = core.lexical_analyzer(line)
        self.w = ''

    def next(self):
        '''
        相当于next(w)
        '''
        self.w = self.analyzer.getToken()

    def analyse(self):
        self.next()
        self.E()
        if self.w == '#':
            print('OK,no error found.')
        else:
            print('error in Z->E!')
            print('w = {}'.format(self.w))
            exit()

    def E(self):
        self.T()
        self.E1()

    def E1(self):
        if self.w == 'w0':
            self.next()
            self.T()
            self.E1()

    def T(self):
        self.F()
        self.T1()
        return

    def T1(self):
        if self.w == 'w1':
            self.next()
            self.F()
            self.T1()

    def F(self):
        if self.w == 'I':
            self.next()
        elif self.w == '(':
            self.next()
            self.E()
            if self.w == ')':
                self.next()
            else:
                print('error in F->(E)!')
                print('w = {}'.format(self.w))
                exit()
        else:
            print('error in F->(E)!')
            print('w = {}'.format(self.w))
            exit()


class LL_1():
    def __init__(self, line):
        self.analyzer = core.lexical_analyzer(line)
        self.w = ''
        self.stack = []
        self.map = {
            ('E', 'I'): ['T', 'E1'],
            ('E', '('): ['T', 'E1'],
            ('E1', 'w0'): ['w0', 'T', 'E1'],
            ('E1', ')'): [],
            ('E1', '#'): [],
            ('T', 'I'): ['F', 'T1'],
            ('T', '('): ['F', 'T1'],
            ('T1', 'w0'): [],
            ('T1', 'w1'): ['w1', 'F', 'T1'],
            ('T1', ')'): [],
            ('T1', '#'): [],
            ('F', 'I'): ['I'],
            ('F', '('): ['(', 'E', ')']
        }
        self.VT = ['I', '(', ')', 'w0', 'w1']
        self.VN = ['E', 'E1', 'T', 'T1', 'F']

    def next(self):
        '''
        相当于next(w)
        '''
        self.w = self.analyzer.getToken()

    def analyse(self):
        self.stack.append('#')
        self.stack.append('E')
        self.next()
        while True:
            tmp = self.stack.pop()
            if tmp in self.VT:
                if self.w == tmp:
                    self.next()
                    continue
                else:
                    print('error, stack[-1]!=w!')
                    exit()
            elif tmp in self.VN:
                if (tmp, self.w) in self.map.keys():
                    # 逆序压栈
                    for item in reversed(self.map[(tmp, self.w)]):
                        self.stack.append(item)
                else:
                    print('error, no {} key in map!'.format((tmp, self.w)))
                    exit()
            else:
                if self.w == '#':
                    print('OK,no error found.')
                    return


if __name__ == '__main__':
    recursive_descent = recursive_descent('((1+2-3*4)-5)#')
    print('recursive descent analyse:')
    recursive_descent.analyse()
    LL_1 = LL_1('((1+2-3*4)-5)#')
    print('LL(1) analyse:')
    LL_1.analyse()
