class Robot:
    # TODO: x, y (0, 100)
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.lastPath = []
        self.lastPath.append(coord)
        # self.startCoord = coord
    
    def move(self, directions):
        self.lastPath.clear()
        self.lastPath.append((self.x, self.y))
        for d in directions:
            if str(d) == 'N':
                self.y += 1
                if self.y > 100:
                    self.y = 100
                self.lastPath.append((self.x, self.y))
            elif str(d) == 'S':
                self.y -= 1
                if self.y < 0:
                    self.y = 0
                self.lastPath.append((self.x, self.y))
            elif str(d) == 'W':
                self.x -= 1
                if self.x < 0:
                    self.x = 0
                self.lastPath.append((self.x, self.y))
            elif str(d) == 'E':
                self.x += 1
                if self.x > 100:
                    self.x = 100
                self.lastPath.append((self.x, self.y))
        return self.lastPath[-1]
    
    def path(self):
        return self.lastPath



if __name__ == '__main__':
    r = Robot((0, 0))
    print(r.path())
    print('-------------------')
    print(r.move('NENW'))
    print(*r.path())
    print('-------------------')
    print(r.move('EESSWW'))
    print(r.path())


