#!/usr/bin/python
from lexical_analyzer import core


class recursive_descent():
    '''
    递归下降子程序分析法
    '''

    def __init__(self, line):
        self.analyzer = core.lexical_analyzer(line)
        self.w = ''

    def Z(self):
        self.w = self.analyzer.getToken()
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
            self.w = self.analyzer.getToken()
            self.T()
            self.E1()

    def T(self):
        self.F()
        self.T1()
        return

    def T1(self):
        if self.w == 'w1':
            self.w = self.analyzer.getToken()
            self.F()
            self.T1()

    def F(self):
        if self.w == 'I':
            self.w = self.analyzer.getToken()
        elif self.w == '(':
            self.w = self.analyzer.getToken()
            self.E()
            if self.w == ')':
                self.w = self.analyzer.getToken()
            else:
                print('error in F->(E)!')
                print('w = {}'.format(self.w))
                exit()
        else:
            print('error in F->(E)!')
            print('w = {}'.format(self.w))
            exit()


if __name__ == '__main__':
    test = recursive_descent('((1+2-3*4)-5)#')
    test.Z()
