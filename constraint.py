import grid
import base_tiles

class GridRule( object ):
    def isValid( grid ):
        return true

class TokenRule( object ):
    def isValid( grid, point, token ):
        return true

class CheckersBoard( GridRule ):
    def isValid( grid ):
        for x, y in grid.points():
            if x % 2 == 0:
                if y % 2 == 0: 
                    if grid.get(x, y).content != '.':
                        return false


if __name__ == '__main__':
    g = grid.Grid(10, 5, base_tiles.TokenTile('.') )

    print g
