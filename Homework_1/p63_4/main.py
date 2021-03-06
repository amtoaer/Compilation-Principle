#!/usr/bin/python
# 简单的c语言词法分析器
# 种别码规则：标识符为0，关键字依次从1到6，界符、运算符依次从7到29，整数为30
# 关键字
keyWord = ['main', 'int', 'if', 'else', 'while', 'do']
# 界符、运算符
symbol = ['<', '>', '!=', '>=', '<=', '==', ',', ';',
          '(', ')', '{', '}', '+', '-', '*', '/', '=', '+=', '-=', '*=', '/=', '++', '--']
# 构造可接受字符的符号表
tmp = set()
for item in symbol:
    for char in item:
        tmp.add(char)


def handleSubStr(content, pos):
    # 跳过空白字符和换行字符
    while content[pos] == ' ' or content[pos] == '\n':
        pos += 1
        # 判断是否越界
        if pos >= len(content):
            return False
    # 数字开头（只考虑整型）
    if content[pos].isdigit():
        token = int(content[pos])
        while pos < len(content):
            pos += 1
            if content[pos].isdigit():
                token = token * 10 + int(content[pos])
            else:
                print('({},30)'.format(token))
                return pos
    # 字母开头
    elif content[pos].isalpha():
        token = content[pos]
        while pos < len(content):
            pos += 1
            if content[pos].isdigit() or content[pos].isalpha():
                token += content[pos]
            else:
                # 判断是关键字还是自定义标识符
                if token in keyWord:
                    print('({},{})'.format(token, keyWord.index(token)+1))
                else:
                    print('({},0)'.format(token))
                return pos
    elif content[pos] in tmp:
        token = content[pos]
        while(pos < len(content)):
            pos += 1
            # 读取多字符界符的逻辑：如果继续读取后的结果仍然在symbol集合中则读取，否则不读
            if content[pos] in tmp and token + content[pos] in symbol:
                token += content[pos]
            else:
                if token in symbol:
                    print('({},{})'.format(token, len(
                        keyWord)+symbol.index(token)+1))
                    return pos
                else:
                    break
    else:
        print('存在不合法字符，正在退出...')
        return False
    print(token)
    print(tmp)
    print('程序出现错误，请检查源代码是否正确。\n正在退出...')
    return False


def handleStr(content):
    pos = 0
    while True:
        pos = handleSubStr(content, pos)
        # 如果程序正常结束/出现错误则跳出循环
        if not pos:
            break


def main():
    # 读取文件
    with open('/home/jeasonlau/Documents/repositories/CP/p63_4/test.c', 'r') as f:
        content = f.read()
    # 处理字符串
    handleStr(content)


if __name__ == '__main__':
    main()
