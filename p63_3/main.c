#include <stdio.h>
/*
    GetChar():读入下一个输入字符到ch中
    GetBC():检查输入字符是否为空格，如果是空格则调用GetChar直至非空
    Concat():将ch中的字符连接到strToken之后
*/
char* string = "    this is a   test.";
char ch = ' ';
int stringIndex = 0;
int tokenIndex = 0;
char strToken[10];
void GetChar()
{
    ch = string[stringIndex++];
    printf("调用GetChar()\n");
}
void GetBC()
{
    printf("调用GetBC()\n");
    while (string[stringIndex] == ' ' || string[stringIndex] == '\n') {
        GetChar(string);
    }
    printf("GetBC()执行完毕\n");
}
void Concat()
{
    strToken[tokenIndex++] = ch;
    printf("调用Concat()\n");
}
int main()
{
    // 忽略连续空格
    printf("需要处理的字符串为\n%s\n", string);
    GetBC();
    // 读取't'
    GetChar();
    // 打印't'
    printf("输出ch内的字符\n");
    printf("%c\n", ch);
    // 将't'连接到strToken
    Concat();
    // 读取'h'
    GetChar();
    // 将'h'连接到strToken
    Concat();
    //打印"th"
    printf("打印strToken字符串\n");
    printf("%s\n", strToken);
    return 0;
}
