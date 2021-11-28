class test():
    a = 0
    def __init__(self, a = -1) -> None:
        self.a = a
    def changeA(self, a):
        self.a = a

test1 = test()
test1.changeA(10)

test2 = test()
print(test2.a)