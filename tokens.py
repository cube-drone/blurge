from token_grid import TokenGrid
from token_tiles import SingleTokenTile 

class Token( object ):
    def name( self ):
        return "Token"

    def isValid( self, grid, point ):
        """ Takes a grid object and a tuple point (x, y) """
        return true
    
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        return self

    def existsOnTheBoard( self, grid ):
        """ Returns True if this token exists anywhere on the grid. """
        for grid_x, grid_y in grid.points():
            if self.atPoint( grid, (grid_x, grid_y) ):
                return True
        return False

    def atPoint( self, grid, point ):
        """ Tests if this token exists at a point on the board. """ 
        return grid.isTokenAtPoint( self, point )

    def atPointInList( self, grid, list_of_points ):
        """ Tests if this token exists at any of these points on the board. """
        return grid.isTokenAtPointInList( self, list_of_points )

    def __repr__(self):
        return self.name()

class InvisibleToken( Token ):
    def name( self ):
        return "InvisibleToken" 

class Checker( Token ):
    def name( self ):
        return "Checker" 

    def isValid( self, grid, point ):
        """ When x is odd, y must be even. When x is even, y must be odd. """
        x, y = point
        if x % 2 == 0:
            if y % 2 == 0:
                return False
        if x % 2 == 1:
            if y % 2 == 1:
                return False
        return True

def __checker_test():
    g = TokenGrid(10, 10)

    assert( not Checker().isValid( g, (0, 0) ))
    assert(  Checker().isValid( g, (0, 1) ))
    assert( not Checker().isValid( g, (0, 2) ))
    assert(  Checker().isValid( g, (0, 3) ))
    assert( not Checker().isValid( g, (0, 4) ))
    assert(  Checker().isValid( g, (1, 0) ))
    assert( not Checker().isValid( g, (1, 1) ))
    assert(  Checker().isValid( g, (1, 2) ))
    assert( not Checker().isValid( g, (1, 3) ))
    assert(  Checker().isValid( g, (1, 4) ))

class Rook( Token ):
    def name( self ):
        return "Rook" 
    def isValid( self, grid, point):
        """ Object must be horizontal or vertical to another rook. """
        
        # If there isn't a rook on the board, there won't ever be a way to place one! 
        if not self.existsOnTheBoard( grid ): 
            return True
        
        x, y = point 
        for grid_x, grid_y in grid.points():
            if grid_x == x:
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return True
            if grid_y == y:
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return True
        return False

def __rook_test():
    g = TokenGrid(10, 10)
    
    assert( Rook().isValid( g, (3, 3 ) ) )
    g.get( 3, 3 ).token = Rook()
    
    assert( Rook().isValid( g, (3, 1 ) ) )
    assert( Rook().isValid( g, (3, 7 ) ) )
    assert( Rook().isValid( g, (7, 3 ) ) )
    assert( Rook().isValid( g, (2, 3 ) ) )
    assert( not Rook().isValid( g, (5, 5) ) )


class Knight( Token ):
    def name( self ):
        return "Knight" 
    def isValid( self, grid, point):
        """ Object must be two-up-and-one-over in any direction to another knight. """
        
        if not self.existsOnTheBoard( grid ): 
            return True
        
        x, y = point

        potential_knight_locations = [ (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1 ), 
                                        (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2) ] 
        
        for knight_point in potential_knight_locations: 
            kx, ky = knight_point
            if self.atPoint( grid, (kx, ky) ):
                return True

        return False


def __knight_test():
    g = TokenGrid(10, 10)
    
    assert( Knight().isValid( g, (5, 5 ) ) )
    g.get( 5, 5 ).token = Knight()
    
    assert( Knight().isValid( g, (7, 6 ) ) )
    assert( Knight().isValid( g, (6, 7 ) ) )
    assert( Knight().isValid( g, (4, 7 ) ) )
    assert( Knight().isValid( g, (7, 4 ) ) )
    assert( not Knight().isValid( g, (3, 5) ) )

    g.get( 9, 9 ).token = Knight()
    assert( Knight().isValid( g, (7, 8) ) )
    assert( not Knight().isValid( g, (7, 7) ) )

class Pawn( Token ):
    def name( self ):
        return "Pawn"
    def isValid( self, grid, point):
        """ A pawn can be placed adjacent to any other piece, or diagonal to any other pawn. """ 
        x, y = point
        token_locations = [ (x+1, y), (x, y+1), (x-1, y), (x, y-1) ] 
        pawn_locations = [ (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1) ]

        if self.atPointInList( grid, pawn_locations ):
            return True

        

        for token_point in token_locations:
            tx, ty = token_point
            if grid.isAnyTokenAtPoint( (tx, ty) ) and not self.atPoint( grid, (tx, ty) ):
                return True

def __pawn_test():
    g = TokenGrid(10, 10)
    
    assert( Knight().isValid( g, (5, 5 ) ) )
    g.get( 5, 5 ).token = Knight()
    
    assert( Pawn().isValid( g, (5, 6 ) ) )
    assert( Pawn().isValid( g, (6, 5 ) ) )
    assert( Pawn().isValid( g, (4, 5 ) ) )
    assert( Pawn().isValid( g, (5, 4 ) ) )
    assert( not Pawn().isValid( g, (3, 5) ) )

    g.get( 6, 5 ).token = Pawn()
    assert( Pawn().isValid( g, (7, 6 ) ) )
    assert( Pawn().isValid( g, (5, 4 ) ) )
    assert( Pawn().isValid( g, (7, 4 ) ) )
    assert( Pawn().isValid( g, (5, 6 ) ) )
    assert( not Pawn().isValid( g, ( 6, 6 ) ) )

def King( Token ):
    def name( self ):
        return "King"
    def isValid( self, grid, point ):
        """ A king cannot be placed adjacent to any other piece, nor can any other piece be placed adjacent to a king."""
        x, y = point

if __name__ == '__main__':
    __checker_test()
    __rook_test()
    __knight_test()
    __pawn_test()
