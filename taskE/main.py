from inspect import getsource
import inspect
from sys import stdin


def main() -> None:
    l = stdin.readline().rstrip('\n').split(' ')
    Na, Nb, Nc = int(l[0]), int(l[1]), int(l[2])
    versions: list = []
    rules: list = []

    for i in range(1, Na + 1):
        for j in range(1, Nb + 1):
            for k in range(1, Nc + 1):
                versions.append((i, j, k))

    for _ in range(int(input())):
        l = stdin.readline().rstrip('\n').split(' ')

        mod1 = int(l[0]) - 1
        ver1 = int(l[1])
        mod2 = int(l[2]) - 1
        ver2 = int(l[3])

        # if s[mod1] >= ver1:
        #     if s[mod2] >= ver2:
        #         True
        # True

        def rule(s) -> bool:
            print(f'checking {s} with({mod1}, {ver1}, {mod2}, {ver2})')
            # if s[mod1] < ver1: return True
            if s[mod1] >= ver1:
                return s[mod2] >= ver2
            else:
                return False

        # rules.append(lambda s: s[mod1] >= ver1 and s[mod2] >= ver2)
        rules.append(rule)

    count = 0
    res = []
    for sys in versions:
        result = True
        for r in rules:
            result = result and r(sys)
            # res.append(r(sys))
            # print(r(sys))
            # if r(sys): count += 1
        if result:
            count += 1
            # print(sys)
    print(count)
    # print(res.count(True))

if __name__ == '__main__':
    main()