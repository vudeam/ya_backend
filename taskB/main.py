from sys import stdin
from collections import namedtuple


Ingredient = namedtuple('Ingredient', ['name', 'count', 'symbol'])


class Glass:
    def __init__(self, n, m) -> None:
        self.nlines = n
        self.mchars = m
        self.glass: list[str] = []
        self.ingredients: list[Ingredient] = []

    def read_glass(self) -> None:
        if not self.nlines or not self.mchars:
            raise ValueError('Params must be set')
        for n in range(self.nlines):
            self.glass.append(stdin.readline().rstrip('\n'))
            # self.glass.append(stdin.readline().split())

    def read_ingredients(self) -> list:
        for i in range(int(input())):
            l = stdin.readline().rstrip('\n').split(' ')
            self.ingredients.append(
                Ingredient(l[0], int(l[1]), l[2])
            )
        return self.ingredients

    def fill_glass(self) -> None:
        if len(self.ingredients) < 1:
            raise ValueError('Input ingredients first')
        off = 1
        glass = []
        for ing in self.ingredients:
            for line in range(ing.count):
                layer = self.glass[-(1 + off + line)].replace(' ', ing.symbol)
                # self.glass[::-1][off + line] = layer
                self.glass[-(1 + off + line)] = layer
                #print(f'Filling with: {ing}; {layer}')
                #print(f'Filled line: {self.glass[-(1 + off + line)]}')
                # print(f'Filled line: {self.glass[::-1][off + line]}')
                # off += 1
            # off = ing.count + 1
            off += ing.count

    def __str__(self) -> None:
        result = ''
        for line in self.glass:
            result += (line + '\n')
        return result


def main() -> None:
    nm = stdin.readline()
    n = int(nm.split(' ')[0])
    m = int(nm.split(' ')[1])

    glass = Glass(n, m)
    glass.read_glass()
    #print(glass)

    glass.read_ingredients()

    glass.fill_glass()
    print(glass)


if __name__ == '__main__':
    main()
