class AbstractCat:
    def __init__(self):
        self.weight = 0
        self.spare = 0

    def eat(self, food):
        self.spare += int(food)
        self.weight += self.spare // 10
        if self.weight > 100:
            self.weight = 100
        self.spare %= 10
    
    def __str__(self):
        return f'{self.__class__.__name__} ({self.weight})'


class Kitten(AbstractCat):
    def __init__(self, _weight):
        self.weight = _weight
        self.spare = 0
    
    def meow(self):
        return 'meow...'
    
    def sleep(self):
        return 'Snore' * (self.weight // 5)


class Cat(Kitten):
    def __init__(self, _weight, _name):
        self.weight = _weight
        self.spare = 0
        self.name = _name
    
    def meow(self):
        return 'MEOW...'
    
    def get_name(self):
        return self.name
    
    def catch_mice(self):
        return 'Got it!'

        
if __name__ == '__main__':
    # ac = AbstractCat()
    # # for i in range(25):
    # ac.eat(21)
    # print(str(ac))
    # ac.eat(9)
    # print(str(ac))

    # kt = Kitten(27)
    # print(kt.sleep())

    # ct = Cat(1, 'Муся')
    # ct.eat(70)
    # print(str(ct))
    # print('weight:', ct.weight)
    # print(ct.catch_mice())
    # print(ct.get_name())
    kit = Kitten(15)
    kit.eat(24)
    print(kit)
    cat = Cat(41, 'Molly')
    print(cat.catch_mice())
    print(cat)
