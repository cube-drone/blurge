from token_grid import TokenGrid
from grid import adjacentPoints, isDiagonalPoint
from token_tiles import SingleTokenTile 
import copy
import random

class Token( object ):
    def name( self ):
        return "Token"

    def isValid( self, grid, point ):
        """ Takes a grid object and a tuple point (x, y) """
        return True
    
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        return self

    def existsOnTheBoard( self, grid ):
        """ Returns True if this token exists anywhere on the grid. """
        for point in grid.points():
            if self.atPoint( grid, point ):
                return True
        return False

    def atPoint( self, grid, point ):
        """ Tests if this token exists at a point on the board. """ 
        return grid.isTokenAtPoint( self, point )

    def atPointInList( self, grid, list_of_points ):
        """ Tests if this token exists at any of these points on the board. """
        return grid.isTokenAtPointInList( self, list_of_points )

    def __repr__(self):
        return self.name()[0]

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

    assert( not g.placeToken( Checker(), (0, 0 ) ) )
    assert( g.placeToken( Checker(), (0, 1 ) ) )
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
    
    assert( g.placeToken( Rook(), (3,3) ) )
    
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
    
    assert( g.placeToken( Knight(), (5, 5) ) ) 
    
    assert( Knight().isValid( g, (7, 6 ) ) )
    assert( Knight().isValid( g, (6, 7 ) ) )
    assert( Knight().isValid( g, (4, 7 ) ) )
    assert( Knight().isValid( g, (7, 4 ) ) )
    assert( not Knight().isValid( g, (3, 5) ) )

    g.setToken( Knight(), (9, 9 ) )  
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
    
    assert( g.placeToken( Knight(), (5,5) ) ) 
    
    assert( Pawn().isValid( g, (5, 6 ) ) )
    assert( Pawn().isValid( g, (6, 5 ) ) )
    assert( Pawn().isValid( g, (4, 5 ) ) )
    assert( Pawn().isValid( g, (5, 4 ) ) )
    assert( not Pawn().isValid( g, (3, 5) ) )

    assert( g.placeToken( Pawn(), (6,5 ) ) )
    assert( Pawn().isValid( g, (7, 6 ) ) )
    assert( Pawn().isValid( g, (5, 4 ) ) )
    assert( Pawn().isValid( g, (7, 4 ) ) )
    assert( Pawn().isValid( g, (5, 6 ) ) )
    assert( not Pawn().isValid( g, ( 6, 6 ) ) )

class King( Token ):
    def name( self ):
        return "King"
    def isValid( self, grid, point ):
        """ A king cannot be placed adjacent to any other piece, nor can any other piece be placed adjacent to a king."""
        if( grid.isAnyTokenAtPointInList( adjacentPoints( point ) ) ):
            return False
        return True 
    
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        
        points = adjacentPoints( point )
        for point in points:
            grid.setToken( InvisibleToken(), point )  

        return self

def __king_test():
    g = TokenGrid( 10, 10 )
    assert( King().isValid( g, (1,1 ) ) ) 
    assert( g.placeToken( King(), (1, 1) ) ) 
    assert( g.placeToken( King(), (5, 5) ) )
    assert( not g.placeToken( King(), (5, 6) ) )
    assert( not g.placeToken( King(), (6, 6) ) )
    assert( not g.placeToken( King(), (0, 0) ) )

class Bishop( Token ):
    def name( self ):
        return "Bishop" 
    def isValid( self, grid, point ):
        """ A bishop can only be placed diagonally to another Bishop. """
        
        # If there isn't a bishop on the board, there won't ever be a way to place one! 
        if not self.existsOnTheBoard( grid ): 
            return True
        
        for grid_x, grid_y in grid.points():
            if isDiagonalPoint( point, (grid_x, grid_y) ):
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return True
             
        return False

def __bishop_test():
    g = TokenGrid( 10, 10 )
    assert( g.placeToken( Bishop(), (5, 5) ) )
    assert( g.placeToken( Bishop(), (8, 8) ) )
    assert( g.placeToken( Bishop(), (3, 7) ) )
    assert( not g.placeToken( Bishop(), (1, 2 ) ) ) 

class Parasite( Token ):
    def name( self ):
        return "Parasite" 
    def isValid( self, grid, point ):
        """ A parasite can be adjacent to any token but not another parasite. """
        
        adjacent_points = adjacentPoints( point ) 

        if grid.isAnyTokenAtPointInList( adjacent_points ) and not self.atPointInList( grid, adjacent_points ):
            return True
        else:
            return False

def __parasite_test():
    g = TokenGrid( 10, 10 )
    assert( g.placeToken( Bishop(), (5, 5) ) )
    assert( g.placeToken( Parasite(), (5, 6) ) )
    assert( not g.placeToken( Parasite(), (6, 6) ) )


class Joker( Token ):
    def name( self ):
        return "Joker" 
    def isValid( self, grid, point ):
        """ No pattern here. Randomness. """
        return random.choice( [ True, False ] ) 

def __joker_test():
    g = TokenGrid( 100, 10 )
    
    for point in g.points():
        g.placeToken( Joker(), point ) 

    counter = 0 
    for point in g.points():
        if g.isAnyTokenAtPoint( point ): 
            counter += 1
    assert( counter > 0 and counter < 1000 )


class Bomb( Token ):
    def name( self ):
        return "Bomb"
    def isValid( self, grid, point ):
        return True

    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        
        points = adjacentPoints( point )
        for point in points:
            grid.clearToken( point )  

        return self

def __bomb_test():
    g = TokenGrid( 10, 10 )

    assert( g.placeToken( Rook(), (4,6) ) )
    assert( g.placeToken( Rook(), (5,6) ) )
    assert( g.placeToken( Rook(), (6,6) ) )
    assert( g.placeToken( Rook(), (4,5) ) )
    assert( g.placeToken( Rook(), (6,5) ) )
    assert( g.placeToken( Rook(), (4,4) ) )
    assert( g.placeToken( Rook(), (5,4) ) )
    assert( g.placeToken( Rook(), (6,4) ) )
    
    assert( g.placeToken( Bomb(), (5,5) ) ) 

    assert( not Rook().existsOnTheBoard( g ) )

class Glob( Token ):
    def name( self ):
        return "Glob" 
    def isValid( self, grid, point ):
        if not self.existsOnTheBoard( grid ): 
            return True
        if self.atPointInList( grid, adjacentPoints( point ) ):
            return True

def __glob_test():
    g = TokenGrid( 10, 10 )

    assert( g.placeToken( Glob(), (5, 5) ) )
    assert( g.placeToken( Glob(), (5, 6) ) )
    assert( g.placeToken( Glob(), (5, 7) ) )
    assert( g.placeToken( Glob(), (6, 8) ) )
    assert( not g.placeToken( Glob(), (1,1) ) )
    assert( g.frequencyHistogram()['Glob'] == 4 ) 

class Brick( Token ):
    def name( self ):
        return "Brick"
    def isValid( self, grid, point ):
        """ A brick cannot be placed adjacent to any piece. """
        if( grid.isAnyTokenAtPointInList( adjacentPoints( point ) ) ):
            return False
        return True 
    
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
       
        points = adjacentPoints( point )
        for brick_point in points:
            x,y = brick_point
            grid.setToken( Brick(), (x,y) )

        return self

def __brick_test():
    g = TokenGrid( 10, 10 )
    assert( g.placeToken( Brick(), (5, 5) ) ) 
    assert( g.frequencyHistogram()['Brick'] == 9 ) 

# class Wallflower( Token ):
# class UnRook( Token )
# class UnBishop( Token )

tokens = [ 
            Checker(), 
            Rook(), 
            Knight(), 
            Pawn(), 
            King(), 
            Bishop(),
            Parasite(),
            Joker(),
            Bomb(),
            Glob(),
            Brick() ]

def selectRandomToken():
    return random.choice( tokens )

def selectRandomNTokens( n ):
    if n >= len( tokens ):
        return copy.deepcopy( tokens )
    if n <= 0:
        return [] # and, also, what? 
    random_tokens = []
    selection_space = copy.deepcopy( tokens )
    for i in range(0, n ):
        temp_token =  random.choice( selection_space )
        random_tokens.append( temp_token )
        selection_space.remove( temp_token )
    return random_tokens 

def __random_token_test():
    print selectRandomNTokens( 5 )

if __name__ == '__main__':
    __checker_test()
    __rook_test()
    __knight_test()
    __pawn_test()
    __king_test()
    __bishop_test()
    __parasite_test()
    __joker_test()
    __bomb_test()
    __glob_test()
    __brick_test()

    __random_token_test()
