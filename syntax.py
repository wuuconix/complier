from copy import deepcopy
from lexicalForsyn import getToken

variables = ['P', 'D', 'S', 'L', 'C', 'E', 'T', 'F'] #语法变量们
terminals = [';', 'int', 'float', 'if', 'else', 'while', '=', '(', ')', '>', '<', '==', '+', '-', '*', '/', 'id', 'digits', '$'] #最后加了个$，当作terminal
first = {'P': ['int', 'float', 'id', 'if', 'while'], \
         'D': ['int', 'float', 'ε'],\
         'S': ['id', 'if', 'while'],\
         'L': ['int', 'float'],\
         'C': ['(', 'id', 'digits'],\
         'E': ['(', 'id', 'digits'],\
         'T': ['(', 'id', 'digits'],\
         'F': ['(', 'id', 'digits']}
follow = {'P': ['$'], \
         'D': ['id', 'if', 'while'],\
         'S': ['$', ';'], \
         'L': ['id'],\
         'C': [')'],\
         'E': [';', '>', '<', '==', '+', '-', ')'],\
         'T': [';', '>', '<', '==', '+', '-', ')', '*', '/'],\
         'F': [';', '>', '<', '==', '+', '-', ')', '*', '/']}
symbols = variables + terminals #所有的符号
output = ""

class Item(): #项类，包含产生式头，产生式体 以及项集中点的位置
    head = ""
    body = []
    dot = 0

    def __init__(self, head, body, dot = 0):
        self.head = head
        self.body = body
        self.dot = dot
    def __eq__(self, other): #重写相同，判断两个项是否相同
        return self.body == other.body and self.body == other.body and self.dot == other.dot
    def eqProduction(self, other): #判断两者的产生式是否相同
        if self.head == other.head and self.body == other.body:
            return True
        else:
            return False
    def displayItem(self):
        tmp = deepcopy(self.body)
        tmp.insert(self.dot, "‧")
        body = " ".join(tmp)
        global output
        if "ε" in body:
            print(f"{self.head}-> ‧")
            output += f"{self.head}-> ‧<br>\n"
        else:
            print(f"{self.head}-> {body}")
            output += f"{self.head}-> {body}<br>\n"   
    def getExpect(self): #把产生式体点后面的字符拿出
        if self.dot >= len(self.body):
            return None
        else:
            return self.body[self.dot]
    def getExpectVari(self): #点后面的语法变量
        if self.dot >= len(self.body):
            return None
        else:
            if self.body[self.dot] in variables:
                return self.body[self.dot]
            else:
                return None
    def accDot(self): #项中的点向后移动1
        if self.dot < len(self.body):
            self.dot += 1
        
class Items(): #项集
    id = 0 #项集编号，比如I0
    itemList = []
    goto = {} #记录在输入某符号后到达的项集id

    def __init__(self):
        global ids
        self.itemList = []
        self.id = -1
        self.goto = {}
    def __eq__(self, other) -> bool:
        if self.isSubItems(other.itemList) and other.isSubItems(self.itemList): #互为子集则相同
            return True
    def changeId(self, id: int):
        self.id = id
    def pushItem(self, item): #添加
        tmp = deepcopy(item)
        if not self.haveItem(tmp):
            self.itemList.append(tmp)
    def pushItems(self, items): #添加项列表
        for i in items:
            self.pushItem(i)
    def addArrow(self, input, itemId): #增加去处
        self.goto[str(input)] = int(itemId)
    def displayItems(self): #可视化输出项集
        global output
        print(f"项集I{self.id}:")
        output += f'I{self.id}["I{self.id}<br>\n'
        for i in self.itemList:
            i.displayItem()
        output += f'"]\n'
    def haveItem(self, item): #判断该项集中有无某个 项，若有则返回真
        if item in self.itemList:
            return True
        else:
            return False
    def isSubItems(self, items): #判断某个项列表是否为子集
        for i in items:
            if not self.haveItem(i):
                return False
        return True
    def getExpectList(self):
        expectList = []
        for i in self.itemList:
            expectList.append(i.getExpect())
        return expectList
    def getReduceList(self): #返回项集中需要回溯的对应下标的列表
        l = []
        for i in self.itemList:
            if i.dot == len(i.body):
                l.append(self.itemList.index(i))
            elif "ε" in i.body: #空产生式不满足上面的条件,但是也需要规约
                l.append(self.itemList.index(i))
        return l

BasicItemsDict = {}
with open("production.txt", "r") as f:
    lines = f.read().split("\n")
    for i in lines:
        head = i.split("→")[0].rstrip()
        body = i.split("→")[1].lstrip().split(" ")
        tmpItem = Item(head, body)
        if head not in BasicItemsDict:
            BasicItemsDict[head] = [tmpItem]
        else:
            BasicItemsDict[head].append(tmpItem)

Productions = [] #存储所有的产生式，具体proid.txt
for key, value in BasicItemsDict.items():
    Productions += BasicItemsDict[key]

def closure(items: list)-> Items():
    newI = Items()
    newI.pushItems(items)
    for i in newI.itemList:
        expect = i.getExpectVari()
        if not expect: #不用再生成了
            pass
        else:
            addedItems = BasicItemsDict[expect]
            if newI.isSubItems(addedItems):
                pass
            else:
                newI.pushItems(addedItems)
    return newI

def goto(items: Items(), symbol: str)-> Items(): #输入一个项集对象，输出转移后的新项集
    exceptList = items.getExpectList()
    if symbol not in exceptList:
        return None
    else:
        initItems = []
        for i in items.itemList:
            if i.getExpect() == symbol:
                tmp = deepcopy(i)
                tmp.accDot()
                initItems.append(tmp)
        return closure(initItems)

#产生集族
num = 0
a = BasicItemsDict["P'"]
a = closure(a)
a.changeId(num)
ItemsList = [a] #集族
for i in ItemsList:
    for j in symbols:
        tmpItems = goto(i, j)
        if tmpItems and tmpItems not in ItemsList:
            num += 1
            tmpItems.changeId(num)
            ItemsList.append(tmpItems)
            i.goto[j] = num
        elif tmpItems and tmpItems in ItemsList:
            i.goto[j] = ItemsList.index(tmpItems)
        else:
            pass

# print(ItemsList)

# for i in ItemsList:
#     i.displayItems()
#     for key, value in i.goto.items():
#         output += f'I{i.id}--"{key}"-->I{value}\n'

# with open("c.txt", "w") as f:
#     f.write(output)


# 生成SLR分析表，包含action和goto两个部分。
Action = []
Goto = []

for i in ItemsList:
    line_action = [-1] * len(terminals)
    line_goto = [-1] * len(variables)
    if i.goto: #有转移
        for key, value in i.goto.items():
            if key in terminals:
                line_action[terminals.index(key)] = f"s{value}"
            else:
                line_goto[variables.index(key)] = f"{value}"
    reduceList = i.getReduceList() #项集内部需要规约的下标
    for j in reduceList:
        reduce = i.itemList[j]
        for k in Productions:
            if k.eqProduction(reduce): #找到规约
                reduceIndex = Productions.index(k)
                head = k.head
                if head == "P'":
                    line_action[terminals.index("$")] = "acc"
                else:
                    for x in follow[head]:
                        line_action[terminals.index(x)] = f"r{reduceIndex}"
    Action.append(line_action)
    Goto.append(line_goto)

token = getToken() #词法分析得到的token序列
inputList = []
for i in token: #关键字和操作符保留，若是标识符和数字则直接写id和digits
    if i[1] in ["keywords", "operator"]:
        inputList.append(i[0])
    elif i[1] in ["id", "digits"]:
        inputList.append(i[1])


inputList.append("$") #以$结尾
statusStack = [0] #状态栈
prefixStack = [] #已经识别的有效前缀
print(f"状态栈     前缀      剩余输入")
while(1):
    print(f"{statusStack}    {prefixStack}    {inputList}")
    input = inputList[0] #输入符号
    status = int(statusStack[-1]) #最上面的状态
    do = Action[status][terminals.index(input)]
    if do == "acc":
        print("分析成功")
        break
    if do == -1:
        print("action时发生错误")
        break
    elif "s" in do:
        statusStack.append(int(do[1:]))
        prefixStack.append(input)
        inputList.remove(input) #输入队列中删除它,因为已经移入prefixStack中了
    elif "r" in do:
        proId = int(do[1:])
        proBody = Productions[proId].body
        proHead = Productions[proId].head
        if "ε" in proBody: #如果是空产生式的规约则不需要弹栈,直接加状态即可
            pass
        else:
            for i in proBody:
                prefixStack.pop() #弹栈
                statusStack.pop()
        prefixStack.append(proHead)
        status = statusStack[-1]
        nextStatus = int(Goto[status][variables.index(proHead)])
        if nextStatus == -1:
            print("goto时发生错误")
            break
        else:
            statusStack.append(nextStatus)