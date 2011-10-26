import copy

class Grid(object):

    def __init__(self, width, height, default_tile):
        self.__matrix = []
        self.width = width
        self.height = height
        for i in range( 0, height ):
            row = line( width, default_tile ) 
            self.__matrix.append(row)

    def __repr__(self):
        temp = ""
        for i in self.rows():
            for j in i:
                temp += str(j) 
            temp += "\n"
        return temp

    def rows(self):
        for i in self.__matrix:
            yield i

    def all(self):
        for i in self.__matrix:
            for j in i:
                yield j

    def get(self,x,y):
        return self.__matrix[self.height-1-y][x]

    def set(self,x,y,thing):
        self.__matrix[self.height-1-y][x] = thing

    def serialize(self):
        return self.matrix

def line( n, thing ):
    """ Create and return an array containing just the one thing, again and again, n times. """
    return [copy.deepcopy(thing) for x in range(0, n)]

class __test_mock_tile:
    def __init__(self):
        self.content = "."
    def __repr__(self):
        return self.content

if __name__ == "__main__":
    g = Grid(10, 5, __test_mock_tile())
    g.get(0,0).content = "4"
    g.get(9,0).content = "5"
    g.get(9,4).content = "2"
    g.get(0,4).content = "1"

    t = __test_mock_tile()
    t.content = "3"
    g.set(4, 2, t)
    print g

    
