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
    
    def displayItem(self):
        tmp = deepcopy(self.body)
        tmp.insert(self.dot, "‧")
        body = " ".join(tmp)
        print(f"{self.head}-> {body}")
        

productions = [] #存基础的项集，实际上就是产生式们，dot都为0

variables = ['P', 'D', 'S', 'L', 'C', 'E', 'T', 'F'] #语法变量们

with open("production.txt", "r") as f:
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

def checkItem(items, item): #判断items中有没有出现过item
    if item in items:
        return False
    else: #如果没有出现过则返回True
        return True
    
def genItem(item): #根据一个项产生出一个项集
    items = [item]
    dotNext = searchItem(item.body[item.dot]) #根据点后面的语法变量产生的dotNext
    if not dotNext:
        return items
    else: #根据dotNext可以找到新的项
        for i in dotNext:
            if checkItem(items, i):
                items.append(i) #列表合并
            else:
                dotNext.remove(i) #如果已经出现过了则删除
        for i in dotNext:
            tmp = genItem(i) #递归调用自身
            for j in tmp:
                if checkItem(items, j):
                    items.append(j)
        return items

I0 = genItem(deepcopy(productions[0]))

for i in I0:
    i.displayItem()
# print(I0)


# for i in I0:
#     i.displayItem()