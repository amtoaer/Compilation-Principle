'''
考虑到实际需求，该部分的词法分析只需要识别类别，故简单实现即可
'''


class lexical_analyzer():
    def __init__(self, line):
        self.__index = 0
        self.__line = line
        self.__length = len(self.__line)

    def getToken(self):
        '''
        返回六种结果： I,(,),w0,w1,#
        '''
        token = ''
        while self.__index < self.__length:
            # 如果是空格或换行符
            if self.__line[self.__index] == ' ' or self.__line[self.__index] == '\n':
                self.__index += 1
                continue
            # 如果开头是字母
            if self.__line[self.__index].isalpha():
                token = self.__line[self.__index]
                self.__index += 1
                while self.__index < self.__length and (self.__line[self.__index].isalpha() or self.__line[self.__index].isdigit()):
                    token += self.__line[self.__index]
                    self.__index += 1
                return 'I'
            # 支持非负实数
            elif self.__line[self.__index].isdigit():
                token = 0
                while self.__index < self.__length and self.__line[self.__index].isdigit():
                    token = token * 10 + int(self.__line[self.__index])
                    self.__index += 1
                    # 遇到小数点
                    if self.__line[self.__index] == '.':
                        # m用于标记小数位数
                        m = 0
                        # self.__index+=1，此时self.__line[self.__index]为小数点后第一位
                        self.__index += 1
                        while self.__index < self.__length and self.__line[self.__index].isdigit():
                            m += 1
                            token = token * 10 + int(self.__line[self.__index])
                            self.__index += 1
                        token = token * pow(10, -m)
                        break
                return 'I'
            elif self.__line[self.__index] == '(':
                self.__index += 1
                return '('
            elif self.__line[self.__index] == ')':
                self.__index += 1
                return ')'
            elif self.__line[self.__index] == '+' or self.__line[self.__index] == '-':
                self.__index += 1
                return 'w0'
            elif self.__line[self.__index] == '*' or self.__line[self.__index] == '/':
                self.__index += 1
                return 'w1'
            elif self.__line[self.__index] == '#':
                self.__index += 1
                return '#'
            else:
                print('unexpected word: {}'.format(self.__line[self.__index]))
                exit()
        return 'finished'
