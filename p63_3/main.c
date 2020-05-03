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
}
void GetBC()
{
    while (string[stringIndex] == ' ' || string[stringIndex] == '\n') {
        GetChar(string);
    }
}
void Concat()
{
    strToken[tokenIndex++] = ch;
}
int main()
{
    // 忽略连续空格
    GetBC();
    // 读取't'
    GetChar();
    // 打印't'
    printf("%c\n", ch);
    // 将't'连接到strToken
    Concat();
    // 读取'h'
    GetChar();
    // 将'h'连接到strToken
    Concat();
    //打印"th"
    printf("%s\n", strToken);
    return 0;
}
