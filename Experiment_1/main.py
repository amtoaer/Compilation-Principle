#!/usr/bin/python
import sys

'''
这是一个c语言的词法分析器，目前已经支持了除浮点数外的大部分情况（并没有，还有很多情况没有支持XD），
支持未闭合的单引号/双引号报错，字符长度不为1/字符串长度为0报错，不合法的字符报错
'''


# 关键字
KT = ['int', 'main', 'void', 'if', 'else', 'char', 'switch']
# 界符
PT = ['<=', '==', '=', '>', '<', '+', '-', '*', '/',
      '{', '}', ',', ';', '(', ')', '[', ']', '++', '--', '+=', '-=', '*=', '/=']
# PTFirst用于保存界符的第一个字符
PTFirst = {item[0] for item in PT}
# 标识符
iT = []
# 字符
cT = []
# 字符串
sT = []
# 常数
CT = []
# 输出结果
tmp = '{}:<{},{}>'
# 缺少符号错误
lack = 'error:{},{} 缺少{}符号.'
# 单引号内字符长度不为1
char = 'error:{},{} 字符长度不为1.'
# 字符串长度为0
string = 'error:{},{} 字符串长度为0.'
# 不合法字符（未被包含在情况内的字符，如^&*等）
invalidChar = 'error:{},{} 出现不合法字符{}.'


def output(token, name, num):
    # 一个简单的对返回结果的封装（主要为了防止频繁的+1）
    return tmp.format(token, name, num+1)


def handleLine(line, count):
    # 用于处理行
    index = 0
    while index < len(line):
        # 如果是空格或换行符
        if line[index] == ' ' or line[index] == '\n':
            index += 1
            continue
        # 如果开头是字母
        if line[index].isalpha():
            token = line[index]
            index += 1
            # 因为结尾必然有\n，所以在这里不需要考虑越界问题
            while line[index].isalpha() or line[index].isdigit():
                token += line[index]
                index += 1
            if token in KT:
                print(output(token, 'KT', KT.index(token)))
            else:
                if token not in iT:
                    iT.append(token)
                print(output(token, 'iT', iT.index(token)))
        # 目前只支持处理正整数
        elif line[index].isdigit():
            token = int(line[index])
            index += 1
            # 此处不判断越界原因同上
            while line[index].isdigit():
                token = token * 10 + int(line[index])
                index += 1
            if token not in CT:
                CT.append(token)
            print(output(token, 'CT', CT.index(token)))

        elif line[index] == '\"':
            token = ''
            index += 1
            while index < len(line) and line[index] != '\"':
                token += line[index]
                index += 1
            # 跳出循环说明要么越界要么找到了双引号，那么如果没有越界则肯定是找到了双引号
            if index != len(line):
                # 首先需要保证字符串非空
                if token:
                    if token not in sT:
                        sT.append(token)
                    print(output(token, 'sT', sT.index(token)))
                    index += 1
                else:
                    print(string.format(count, index))
                    exit()
            else:
                print(lack.format(count, index, '\"'))
                exit()
        # 判断字符基本同上
        elif line[index] == '\'':
            token = ''
            index += 1
            while index < len(line) and line[index] != '\'':
                token += line[index]
                index += 1
            if index != len(line):
                # 在这里需要保证字符长度为1
                if len(token) == 1:
                    if token not in cT:
                        cT.append(token)
                    print(output(token, 'cT', cT.index(token)))
                    index += 1
                else:
                    print(char.format(count, index))
                    exit()
            else:
                print(lack.format(count, index, '\''))
                exit()
        # 判断是否是界符
        elif line[index] in PTFirst:
            token = line[index]
            index += 1
            # 举例：如果能读到<=则肯定不能只读<
            if token + line[index] in PT:
                token += line[index]
                index += 1
            print(output(token, 'PT', PT.index(token)))
        # 如果不是以上情况，则说明遇到了非法字符
        else:
            print(invalidChar.format(count, index, line[index]))
            exit()


def main():
    try:
        print('尝试重定向输出到"./result"中')
        old = sys.stdout
        fileOut = open(
            '/home/jeasonlau/Documents/repositories/CP/Experiment_1/result', 'w')
        # 如果文件能够成功打开，则重定向输出一定成功（成功信息输出在重定向前，防止把成功信息打印到文件中）
        print('重定向输出成功')
        sys.stdout = fileOut
    except:
        print('重定向输出失败，结果打印到标准输出中')
    with open('/home/jeasonlau/Documents/repositories/CP/Experiment_1/test.c', 'r') as f:
        content = f.readlines()
    count = 1
    try:
        for line in content:
            handleLine(line, count)
            count += 1
    except:
        sys.stdout = old
        print('文件处理过程出现错误，请打开输出文件查看详情...')
        exit()
    # 恢复重定向
    sys.stdout = old
    print('文件处理成功，输出处理后的各表信息：')
    print('标识符表：', iT)
    print('字符表：', cT)
    print('字符串表：', sT)
    print('常数表：', CT)


if __name__ == '__main__':
    main()
