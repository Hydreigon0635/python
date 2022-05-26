class SimpleData:
    a = 0
    b = 0
    
    def sum(self):
        return self.a + self.b

    def set(self, a, b):
        self.a = a
        self.b = b

data1 = SimpleData()
data2 = SimpleData()

data1 = SimpleData()
data1.set(1, 2)
data2.set(3, 4)
print(data1.sum())
print(data2.sum())