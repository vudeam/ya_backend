class PearsBasket:
    def __init__(self, _pears):
        self.pears = int(_pears)
    
    def __floordiv__(self, n):
        # baskets = [PearsBasket(self.pears // n) for i in range((self.pears // n)]
        baskets = []
        for i in range((self.pears // n) - 1):
            b = PearsBasket(self.pears // n)
            baskets.append(b)
        ost = n - (self.pears % n)
        if ost > 0:
            p = PearsBasket(ost)
            baskets.append(p)
        return baskets
    
    def __mod__(self, n):
        return self.pears % n
    
    def __add__(self, pb):
        return PearsBasket(self.pears + pb.pears)
    
    def __sub__(self, n):
        self.pears -= n
        if self.pears < 0:
            self.pears = 0

    def __str__(self):
        return str(self.pears)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.pears})'

# b = PearsBasket(17)
# print(b // 4)
# s = b + b
# print([s])

pb = PearsBasket(17)
array = pb // 17
print(array)
pb_2 = PearsBasket(13)
pb_3 = pb + pb_2
print(pb_3)
print(pb_3 % 7)
pb - 2
print([pb])
