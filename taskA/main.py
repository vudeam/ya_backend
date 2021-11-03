from sys import stdin


def change(a: list, i, j) -> list:
    a[i - 1] = a[i - 1] - a[j - 1]
    return a

def medi(a: list) -> int:
    c = a.copy()
    c.sort()
    return c[1]

def index(a: list) -> list:
    m = medi(a)
    idx = []
    for i, v in enumerate(a):
        if v == m:
            idx.append(i + 1)
    return idx

def main() -> None:
    # a = [1, -3, 2]
    # # print(change(a, 2, 1))
    # # print(medi(a))
    # # print(idx([3, 0, 3]))
    a = [int(l) for l in stdin.readline().split(' ')]
    finished = False
    results = []

    for idx, val in enumerate(a):
        # if (val + 1) in index(a):
        if (idx + 1) in index(a): 
            # print('YES')
            results.append((idx, 'YES'))
            continue
        elif not finished:
            for i in range(3):
                for j in range(3):
                    if (val + 1) in index(change(a, i + 1, j + 1)):
                        # print('YES')
                        results.append((idx, 'YES'))
                        finished = True
                    else:
                        # print('NO')
                        results.append((idx, 'NO'))
                        finished = False
            results.append((idx, 'NO'))

    # print(results)
    for i in range(3):
        print(next(r for r in results if r[0] == i)[1])

if __name__ == '__main__':
    main()
