from copy import deepcopy
# 首先需要根据产生式生成一个项集。

class Item(): #项集类，包含产生式头，产生式体 以及项集中点的位置
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
        if "ε" in body:
            print(f"{self.head}-> ‧")
        else:
            print(f"{self.head}-> {body}")
        

productions = [] #存基础的项集，实际上就是产生式们，dot都为0

variables = ['P', 'D', 'S', 'L', 'C', 'E', 'T', 'F'] #语法变量们

ItemsList = [] #记录所有的项集

terminals = [';', 'int', 'float', 'if', 'else', 'while', '=', '(', ')', '>', '<', '==', '+', '-', '*', '/', 'id', 'digits']
with open("/root/complier/production.txt", "r") as f:
    lines = f.read().split("\n")
    for i in lines:
        head = i.split("→")[0].rstrip()
        body = i.split("→")[1].lstrip().split(" ")
        production = Item(head, body)
        productions.append(production)

def searchItem(head): #根据一个产生式头来找到对应的项集
    items = []
    for i in productions:
        if i.head == head:
            items.append(i)
    return items

def haveItem(items, item): #判断items中有没有出现过item
    if item in items:
        return True
    else:
        return False
    
def genItem(item): #根据一个项产生出一个项集
    items = [item]
    dotNext = []
    if item.dot >= len(item.body): #点已经到了最后
        dotNext = []
    else:
        dotNext = searchItem(item.body[item.dot]) #根据点后面的语法变量产生的dotNext
    if not dotNext:
        return items
    else: #根据dotNext可以找到新的项
        for i in dotNext:
            if haveItem(items, i):
                items.append(i) #列表合并
            else:
                dotNext.remove(i) #如果已经出现过了则删除
        for i in dotNext:
            tmp = genItem(i) #递归调用自身
            for j in tmp:
                if haveItem(items, j):
                    items.append(j)
        return items

I0 = genItem(deepcopy(productions[0]))

ItemsList.append(I0)

def accDot(items): #项中的点向后移动1
    for i in items:
        if i.dot < len(i.body):
            i.dot += 1
    return items

def existItems(items): #判断某个项集是否存在过 存在则为True。
    if items in ItemsList:
        return True
    else:
        return False

def allUsed(used): #判断used列表是否已经完全被使用
    if 0 in used:
        return False
    else:
        return True

def judgItem(item): #判断一个项能否继续goto，可以则返回True
    if item.dot == len(item.body):
        return False
    else:
        return True

def nextItems(items): #根据一个项集 生成后面的项集
    global ItemsList
    newItemsList = [] #后继项集的列表
    used = [0] * len(items) #used列表，用来记录项集中哪学项集已经被使用，提升效率，0表示没用过
    for i in items:
        if not judgItem(i) or "ε" in i.body:
            used[items.index(i)] = 1 #不能再生成了也被标记为1，空产生式也被直接标记为已经使用
    while not allUsed(used):
        itemsNow = items[used.index(0)] #现在去处理的项集
        dotNext = itemsNow.body[itemsNow.dot]
        baseItems = [] #记录最基础的项集
        for i in items:
            if i.body[i.dot] == dotNext:
                used[items.index(i)] = 1 #置为1，表示已用
                baseItems.append(i)
        newItems = deepcopy(baseItems) #新项集, 点往后移动1
        newItems = accDot(newItems)
        for i in newItems:
            gen = genItem(i)
            for j in gen:
                if haveItem(newItems, j):
                    newItems.append(j)
        if not existItems(newItems):
            newItemsList.append(newItems)
    if newItemsList: #如果非空
        ItemsList += newItemsList
        print(f"len(ItemLIst): {len(ItemsList)}")
    else:
        return
    for i in newItemsList:
        nextItems(i) #递归调用
    # return newItemsList
    return

def displayItems(items):
    for i in items:
        i.displayItem()

# displayItems(I0)

nextItems(I0)

print(ItemsList)

# print("----")
# tmp = nextItems(I0)
# for i in tmp:
#     displayItems(i)
#     print('-----')