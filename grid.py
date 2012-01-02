import copy
import errors

class Grid(object):
    """ A grid. """

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
        for i, j in self.points():
            yield self.get(i, j)

    def points(self):
        for i in range( 0, self.width ):
            for j in range( 0, self.height ):
                yield (i, j)

    def get(self,x,y):
        """ If you ask for a tile that is out of range, you get a False """
        if y > self.height-1 or y < 0 or x > self.width-1 or x < 0: 
            return False
        return self.__matrix[self.height-1-y][x]

    def set(self,x,y,thing):
        self.__matrix[self.height-1-y][x] = thing

    def serialize(self):
        return self.matrix

def line( n, thing ):
    """ Create and return an array containing just the one thing, again and again, n times. """
    return [copy.deepcopy(thing) for x in range(0, n)]

def adjacentPoints( point ):
    """ Return all points adjacent to the argument. """ 
    x, y = point
    return  [(x-1, y+1), (x, y+1), (x+1, y+1),
             (x-1, y),             (x+1, y),
             (x-1, y-1), (x, y-1), (x+1, y-1) ] 

def isDiagonalPoint( point_one, point_two ):
    """ Returns true if the two points are diagonal to one another. """
    if point_one == point_two: 
        return False

    x1, y1 = point_one
    x2, y2 = point_two
    delta_x = x2 - x1
    delta_y = y2 - y1
    try:
        slope = (delta_x * 1.0) / delta_y
    except ZeroDivisionError:
        return False
    if 0.98 < slope < 1.02 or -0.98 > slope > -1.02:
        return True
    else:
        return False


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
    assert( not g.get(9,5 ) )
    assert( not g.get(10,4 ) )
    assert( not g.get(10,5) )
    assert( not g.get(100, 100) )  

    t = __test_mock_tile()
    t.content = "3"
    g.set(4, 2, t)
    print g

    counter = 0
    for i, j in g.points():
        x = g.get(i, j)
        counter += 1
    
    if not counter == 50:
        raise errors.Hell( "grid.points() should produce 50 points." )
    
    counter = 0 
    for i in g.all():
        counter += 1

    if not counter == 50:
        raise errors.Hell( "grid.all() should produce 50 outputs." ) 
