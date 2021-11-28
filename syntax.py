from copy import deepcopy

variables = ['P', 'D', 'S', 'L', 'C', 'E', 'T', 'F'] #语法变量们
terminals = [';', 'int', 'float', 'if', 'else', 'while', '=', '(', ')', '>', '<', '==', '+', '-', '*', '/', 'id', 'digits']

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

    def displayItem(self):
        tmp = deepcopy(self.body)
        tmp.insert(self.dot, "‧")
        body = " ".join(tmp)
        global output
        if "ε" in body:
            print(f"{self.head}-> ‧")
            output += f"{self.head}-> ‧\n"
        else:
            print(f"{self.head}-> {body}")
            output += f"{self.head}-> {body}\n"   
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
        output += f"项集I{self.id}:\n"
        for i in self.itemList:
            i.displayItem()
        print("-----------------------")
        output += "---------------------\n"
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


BasicItemsDict = {}
with open("/root/complier/production.txt", "r") as f:
    lines = f.read().split("\n")
    for i in lines:
        head = i.split("→")[0].rstrip()
        body = i.split("→")[1].lstrip().split(" ")
        tmpItem = Item(head, body)
        if head not in BasicItemsDict:
            BasicItemsDict[head] = [tmpItem]
        else:
            BasicItemsDict[head].append(tmpItem)

# print(BasicItemsDict)

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
        else:
            pass

print(ItemsList)

for i in ItemsList:
    i.displayItems()

with open("c.txt", "w") as f:
    f.write(output)
# ItemsList.append(a)
# b = goto(a, "L")
# b.displayItems()
# a = Items()
# a.genBasicItems()
# a.displayItems()