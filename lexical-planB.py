# 此程序利用简单的方法实现了词法分析，但是不符合实验一的想法，被搁浅

import re
# filename = input("please input the filename you want to analyse: ")
filename = "1.c"
source = ""
with open(filename, "r") as f:
    source = f.read()

print(f"源码: {source}")

# print(source)
source = source.replace("\n", " ")

operators = ['+', '-', '*', '/', '>', '<', '=', '(', ')', ';', "'",'==', '>=', '<=', '!=']

keywords = ['if' , 'else' , 'while' , 'int' , 'float']

pattern_id = "[a-zA-Z_]+"
pattern_digits = "[0-9]+"

Space_format = "" #对代码进行格式化，在所有运算符符号前后都加上空格，注意对长度为2的运算符的特别处理 方便日后分割

i = 0
while i < len(source):
    if i < len(source) - 2 and source[i: i + 2] in operators:
        Space_format = Space_format + " " + source[i: i + 2] + " "
        i += 2
        continue
    elif source[i: i + 1] in operators:
        Space_format = Space_format + " " + source[i: i + 1] + " "
        i += 1
        continue
    Space_format += source[i: i + 1]
    i += 1

print(f"在运算符前后加入空格: {Space_format}")

tokens = Space_format.split() #Space_format中可能有多个连续的空格，但是split能够正确分割

print(f"利用空格进行分隔：{tokens}")

for i in tokens:
    if i in keywords:
        print(f"< {i}, keywords >")
    elif re.match(pattern_id, i):
        print(f"< {i}, id >")
    elif re.match(pattern_digits, i):
        print(f"< {i}, digits >")
    elif i in operators:
        print(f"< {i}, operators >")
