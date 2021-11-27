# 利用了手动自动机的形式 实现了词法分析

filename = "input.c" #类c程序放里面
source = ""
with open(filename, "r") as f:
    source = f.read() #源代码 字符串

def is_letter(c):
    return c.isalpha() or c == "_"

def is_num(c):
    return c >= '0' and c <= '9'

keywords = ['if' , 'else' , 'while' , 'int' , 'float']

operators = ['+', '-', '*', '/', '>', '<', '=', '(', ')', ';', "'",'==', '>=', '<=', '!=']

result = []

def check_after_letters(c): #检测在一个letters后面的字符正常不正常
    if c in [' ', ';', '\n']: #如果是空格或者回车那再好不过了
        return True
    if is_num(c): #实验的文法要求标识符只有符号或者下划线，没有数字
        return False
    if not c in operators: #其他的诡异的字符直接返回不正常
        return False
    return True

def check_after_digits(c): #检测在一个letters后面的字符正常不正常
    if c in [' ', ';', '\n']:
        return True
    if is_letter(c):
        return False
    if not c in operators:
        return False
    return True

def check_after_operators(c): #检测在一个operators后面的字符正常不正常，操作符后面的字符比较宽泛，大部分都可以
    if c in operators: #如果还是符号，则肯定发生了错误
        return False
    return True
def panic(i): #恐慌模式，发现不正确后找到一个空格或者分号，并返回空格/分号/回车的坐标
    j = i + 1
    while source[j] not in [' ', ';', '\n']:
        j += 1
    return j

def judge_letter(i): #传参是下标，判断从i开始是否为letters, 标识符或者关键字
    j = i + 1
    while is_letter(source[j]):
        j += 1
    if check_after_letters(source[j]):
        letters = source[i: j]
        if letters in keywords:
            temp = (letters, 'keywords')
            result.append(temp)
        else:
            temp = (letters, 'id')
            result.append(temp)
    else:
        j = panic(j) #j为下一个空格或者分号的坐标
        letters_bad = source[i: j] #不合法的letters
        temp = (letters_bad, 'illegle')
        result.append(temp)
    return j
   
def judge_digits(i): #传参是下标，判断从i开始是否为数字
    j = i + 1
    while is_num(source[j]):
        j += 1
    if check_after_digits(source[j]):
        digits = source[i: j]
        temp = (digits, 'digits')
        result.append(temp)
    else:
        j = panic(j)
        digits_bad = source[i: j]
        temp = (digits_bad, 'illegle')
        result.append(temp)
    return j

def judge_operators(i): #  判断从i开始是否为运算符，实际上最长的运算符也才两位
    ops = source[i: i + 2] #取两位，查看是否再操作符列表中
    if ops in operators: #判断是否为长度为2的运算符
        j = i + 2
        if check_after_operators(source[j]):
            temp = (ops, 'operators')
            result.append(temp)
        else:
            j = panic(j)
            ops_bad = source[i: j]
            temp = (ops_bad, 'illegle')
            result.append(temp)
        return j
    else: #说明运算符的长度为1
        ops = source[i: i + 1]
        j = i + 1
        if check_after_operators(source[j]):
            temp = (ops, 'operators')
            result.append(temp)
        else:
            j = panic(j)
            ops_bad = source[i: j]
            temp = (ops_bad, 'illegle')
            result.append(temp)
        return j

def start(): #控制状态判断流程
    i = 0
    while i < len(source):
        c = source[i]
        if c in [" ", "\n"]: #空格和换行则继续
            i += 1
            continue
        if c == ";": #如果是分号，直接添加
            temp = (c, 'operator')
            result.append(temp)
            i += 1
            continue
        if is_letter(c):
            i = judge_letter(i)
        elif is_num(c):
            i = judge_digits(i)
        elif c in operators:
            i = judge_operators(i)
        else: #开局未知字符，直接恐慌处理
            j = panic(i)
            bad = source[i: j]
            temp = (bad, 'illegle')
            result.append(temp)
            i = j

start()
print(result)
