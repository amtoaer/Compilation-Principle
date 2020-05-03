'''
Pascal共有三种注释写法：
    1.{content}
    2.//content
    3.{*content*}
以下分别处理。
注：因为逐行处理的问题，暂不能处理多行注释
'''


def typeOne(tmp, index, count):
    # {}型注释
    while index < len(tmp):
        if tmp[index] == '}':
            return index
        index += 1
    print('第{}行未找到与"{{"相匹配的"}}"，请修改后重试...'.format(count))
    exit()


def typeTwo(tmp):
    # //型注释，在末尾时结束
    return len(tmp)-2


def typeThree(tmp, index, count):
    # (* *)型注释
    while index < len(tmp) - 1:
        # 防止错误越界
        if tmp[index] == '*' and tmp[index+1] == ')':
            return index + 1
        index += 1
    print('第{}行未找到与"(*"相匹配的"*)"，请修改后重试...'.format(count))
    exit()


def getResult(f, count):
    # 处理单行
    tmp = f.readline()
    # 如果读取到文件结尾则返回false
    if not tmp:
        return False
    result = ''
    index = 0
    while index < len(tmp):
        if tmp[index] == '{':
            index = typeOne(tmp, index, count)
        elif tmp[index] == '(':
            if index < len(tmp) - 1:
                if tmp[index + 1] == '*':
                    index = typeThree(tmp, index, count)
                else:
                    result += tmp[index]
            else:
                # 以左括号结尾
                print('第{}行以左括号结尾，请修改后重试...'.format(count))
                exit(0)
        elif tmp[index] == '/':
            if index < len(tmp) - 1:
                if tmp[index + 1] == '/':
                    index = typeTwo(tmp)
                else:
                    result += tmp[index]
            else:
                # 以斜线结尾
                print('第{}行以斜线结尾，请修改后重试...'.format(count))
                exit()
        else:
            result += tmp[index]
        index += 1
    return result


def main():
    # count用于标记行数，方便报错
    count = 1
    f = open('./test.pas', 'r')
    results = []
    result = ''
    while True:
        result = getResult(f, count)
        if result == False:
            break
        results.append(result)
        count += 1
    for index in range(len(results)):
        print('{} {}'.format(index+1, results[index]), end='')


if __name__ == '__main__':
    main()
