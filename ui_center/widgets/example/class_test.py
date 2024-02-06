class A():

    def __init__(self):
        self.aaa = 1  # == setattr(self, "aaa", 1)
        setattr(self, "bbb", 2222)


    def a(self):
        # self.bbb   ==getattr(self, "bbb")
        print(getattr(self, "bbb"))


b = A()
b.a()