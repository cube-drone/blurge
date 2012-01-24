from token_grid import TokenGrid
from grid import adjacentPoints, isDiagonalPoint
from token_tiles import SingleTokenTile 
import copy
import random

class Token( object ):
    def name( self ):
        return u"Token"
    
    def validMemberOfGame( self, ntokens, grid_x, grid_y, tokens ):
        """ Given the parameters, can we have this token in the game? """
        return True
    
    def isRare( self ):
        """ Rare tokens can only be encountered once every 10 turns.  Also, rare
            tokens only turn up with > 5 tokens. """
        return False

    def isValid( self, grid, point ):
        """ Takes a grid object and a tuple point (x, y) """
        
        # No token may be placed next to a King
        adjacent_points = adjacentPoints( point )
        if( grid.isTokenAtPointInList( King(), adjacent_points) ):
            return False

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
    
    def serialize(self): 
        return { 'name':self.name() }


class InvisibleToken( Token ):
    def name( self ):
        return u"InvisibleToken" 
    def validMemberOfGame( self, ntokens, grid_x, grid_y, tokens ):
        """ InvisibleToken is never a valid token to play. """
        return False

class Checker( Token ):
    def name( self ):
        return u"Checker" 

    def isValid( self, grid, point ):
        """ When x is odd, y must be even. When x is even, y must be odd. """
        if not super( Checker, self ).isValid( grid, point ):
            return False
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
        return u"Rook" 
    def isValid( self, grid, point):
        """ Object must be horizontal or vertical to another rook. """
        if not super( Rook, self ).isValid( grid, point ):
            return False
        
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

    #Nothing can be placed next to a king.     
    assert( g.placeToken( King(), (3,8) ) )
    assert( not Rook().isValid( g, (3,9) ) )

class Knight( Token ):
    def name( self ):
        return u"Knight" 
    def isValid( self, grid, point):
        """ Object must be two-up-and-one-over in any direction to another knight. """
        if not super( Knight, self ).isValid( grid, point ):
            return False
        
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

    g.setToken( Knight(), (9, 9 )  ) 
    assert( Knight().isValid( g, (7, 8) ) )
    assert( not Knight().isValid( g, (7, 7) ) )

class Pawn( Token ):
    def name( self ):
        return u"Pawn"
    def isValid( self, grid, point):
        """ A pawn can be placed adjacent to any other piece, or diagonal to any other pawn. """ 
        if not super( Pawn, self ).isValid( grid, point ):
            return False
        
        if not self.existsOnTheBoard( grid ): 
            return True
        
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

    assert( g.placeToken( Pawn(), (6,5 ) ) )
    assert( Pawn().isValid( g, (7, 6 ) ) )
    assert( Pawn().isValid( g, (5, 4 ) ) )
    assert( Pawn().isValid( g, (7, 4 ) ) )
    assert( Pawn().isValid( g, (5, 6 ) ) )
    assert( not Pawn().isValid( g, ( 6, 6 ) ) )

class King( Token ):
    def name( self ):
        return u"King"
    
    def validMemberOfGame( self, ntokens, grid_x, grid_y, tokens ):
        """ The game board must be at least 5x5 for the King to join in the fun. """
        if (grid_x < 5 or grid_y < 5):
            return False
        else:
            return True
    
    def isValid( self, grid, point ):
        """ A king cannot be placed adjacent to any other piece, nor can any other piece be placed adjacent to a king."""
        if not super( King, self ).isValid( grid, point ):
            return False
        if( grid.isAnyTokenAtPointInList( adjacentPoints( point ) ) ):
            return False
        return True 

def __king_test():
    g = TokenGrid( 10, 10 )
    assert( King().isValid( g, (1,1 ) ) ) 
    assert( g.placeToken( King(), (1, 1) ) ) 
    assert( g.placeToken( King(), (5, 5) ) )
    assert( not g.placeToken( King(), (5, 6) ) )
    assert( not g.placeToken( King(), (6, 6) ) )
    assert( not g.placeToken( King(), (0, 0) ) )
    assert( g.placeToken( King(), (3,3) ) )

class Bishop( Token ):
    def name( self ):
        return u"Bishop" 
    def isValid( self, grid, point ):
        """ A bishop can only be placed diagonally to another Bishop. """
        if not super( Bishop, self ).isValid( grid, point ):
            return False
        
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
        return u"Parasite" 
    def isValid( self, grid, point ):
        """ A parasite can be adjacent to any token but not another parasite. """
        if not super( Parasite, self ).isValid( grid, point ):
            return False
        
        if not self.existsOnTheBoard( grid ): 
            return True
        
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
        return u"Joker" 
    def isRare( self ):
        """ The joker's randomness is no fun unless it's rare. """
        return True
    def isValid( self, grid, point ):
        """ No pattern here. Randomness. """
        if not super( Joker, self ).isValid( grid, point ):
            return False
        return random.choice( [ True, True, False ] ) 

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
        return u"Bomb"
    def isRare( self ):
        """ The bomb makes games impossible if it is not rare.  """
        return True
    def isValid( self, grid, point ):
        if not super( Bomb, self ).isValid( grid, point ):
            return False
        return True
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        super( Bomb, self ).afterPlacement( grid, point ) 
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
        return u"Glob" 
    def isValid( self, grid, point ):
        if not super( Glob, self ).isValid( grid, point ):
            return False
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
        return u"Brick"
    def isValid( self, grid, point ):
        """ A brick cannot be placed adjacent to any piece. """
        if not super( Brick, self ).isValid( grid, point ):
            return False
        if( grid.isAnyTokenAtPointInList( adjacentPoints( point ) ) ):
            return False
        return True 
    
    def afterPlacement( self, grid, point ):
        """ Called after the token is placed at a point. """
        super(Brick, self).afterPlacement( grid, point ) 
       
        points = adjacentPoints( point )
        for brick_point in points:
            x,y = brick_point
            grid.setToken( Brick(), (x,y) )

        return self

def __brick_test():
    g = TokenGrid( 10, 10 )
    assert( g.placeToken( Brick(), (5, 5) ) ) 
    assert( g.frequencyHistogram()[Brick().name()] == 9 ) 

class Wallflower( Token ):
    def name( self ):
        return u"A"
    def isValid( self, grid, point ):
        """ A wallflower can only be placed on an edge. """
        if not super( Wallflower, self ).isValid( grid, point ):
            return False
        x, y = point
        if x == 0 or y == 0 or x == grid.width -1 or y == grid.height -1:
            return True
        else:
            return False 

def __wallflower_test():
    g = TokenGrid( 10, 15 )
    assert( not g.placeToken( Wallflower(), (5, 5) ) ) 
    assert( g.placeToken( Wallflower(), (0, 5) ) ) 
    assert( g.placeToken( Wallflower(), (0, 0) ) ) 
    assert( g.placeToken( Wallflower(), (5, 0) ) ) 
    assert( g.placeToken( Wallflower(), (5, 14) ) ) 
    assert( g.placeToken( Wallflower(), (9, 5) ) ) 
    assert( g.placeToken( Wallflower(), (9, 14) ) ) 

class Church( Token ):
    def name( self ):
        return u"B"
    def isValid( self, grid, point ):
        """ A church cannot be diagonal to another church.  """
        if not super( Church, self ).isValid( grid, point ):
            return False
        
        for grid_x, grid_y in grid.points():
            if isDiagonalPoint( point, (grid_x, grid_y) ):
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return False
        return True

def __church_test():
    g = TokenGrid( 10, 10 )
    assert( g.placeToken( Church(), (5, 5) ) )
    assert( not g.placeToken( Church(), (8, 8) ) )
    assert( not g.placeToken( Church(), (3, 7) ) )
    assert( g.placeToken( Church(), (1, 2 ) ) ) 

class State( Token ):
    def name( self ):
        return u"C"
    def isValid( self, grid, point ):
        """ A state cannot be horizontal to another state.   """
        if not super( State, self ).isValid( grid, point ):
            return False
        
        x, y = point 
        for grid_x, grid_y in grid.points():
            if grid_x == x:
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return False
            if grid_y == y:
                if self.atPoint( grid, (grid_x, grid_y) ):
                    return False
        return True

def __state_test():
    g = TokenGrid(10, 10)
    
    assert( g.placeToken( State(), (3,3) ) )
    
    assert( not State().isValid( g, (3, 1 ) ) )
    assert( not State().isValid( g, (3, 7 ) ) )
    assert( not State().isValid( g, (7, 3 ) ) )
    assert( not State().isValid( g, (2, 3 ) ) )
    assert( State().isValid( g, (5, 5) ) )

class Crowd( Token ):
    def name( self ):
        return u"E"
    
    def validMemberOfGame( self, ntokens, grid_x, grid_y, tokens ):
        """ The game board must be at least 5x5 for the Crowd to join in the fun. """
        if (grid_x < 5 or grid_y < 5):
            return False
        else:
            return True
    
    def isValid( self, grid, point ):
        """ A crowd must be placed adjacent to 5 or more pieces. """
        if not super( Crowd, self ).isValid( grid, point ):
            return False
        
        points = adjacentPoints( point )
        
        counter = 0 
        for adjacentPoint in points:
            if grid.isAnyTokenAtPoint( adjacentPoint ):
                counter += 1

        if counter < 5: 
            return False
        return True

def __crowd_test():
    g = TokenGrid(10, 10)
    
    assert( g.placeToken( Rook(), (3,3) ) )
    assert( g.placeToken( Rook(), (3,4) ) )
    assert( g.placeToken( Rook(), (4,3) ) )
    assert( g.placeToken( Rook(), (5,3) ) )
    assert( g.placeToken( Rook(), (5,4) ) ) 
    
    assert( g.placeToken( Crowd(), (4,4) ) )
    assert( not g.placeToken( Crowd(), (6,6) ) )

class Assassin( Token ):
    def name( self ):
        return u"F"
    
    def isRare( self ):
        return True
 
    def isValid( self, grid, point ):
        """ Pretty much always valid. """
        if not super( Assassin, self ).isValid( grid, point ):
            return False
        return True
    
    def afterPlacement( self, grid, point ):
        """ Disappears after placement. """
        grid.clearToken( point )
        grid.setToken( InvisibleToken(), point )

def __assassin_test():
    g = TokenGrid(10, 10)
    
    assert( g.placeToken( Assassin(), (3,3) ) )
    assert( g.placeToken( Assassin(), (5,5) ) )
    assert( g.frequencyHistogram()[InvisibleToken().name()] == 2 ) 

token_dict = {  Checker().name(): Checker(), 
            Rook().name(): Rook(), 
            Knight().name(): Knight(), 
            Pawn().name(): Pawn(), 
            King().name(): King(), 
            Bishop().name(): Bishop(),
            Parasite().name(): Parasite(),
            Joker().name(): Joker(),
            Bomb().name(): Bomb(),
            Glob().name(): Glob(),
            Brick().name(): Brick(),
            Wallflower().name(): Wallflower(),
            Church().name(): Church(),
            State().name(): State(),
            Crowd().name(): Crowd(),
            Assassin().name(): Assassin(),
            InvisibleToken().name(): InvisibleToken() } 

token_array = [value for key, value in token_dict.iteritems()] 

def selectRandomToken():
    return random.choice( tokens )

def selectRandomNTokens( n, grid_x, grid_y ):
    if n >= len( token_array ):
        return copy.deepcopy( token_array )
    if n <= 0:  # We can't return less than zero tokens. 
        return [] 

    random_tokens = []
    selection_space = copy.deepcopy( token_array )
    # If n <= 5, remove Bomb, Joker from selection space. 
    for token in selection_space: 
        if token.isRare() and n < 5:
            selection_space.remove(token) 
    # Select and return n tokens.  
    for i in range(0, n ):
        temp_token =  random.choice( selection_space)
        while not tryToSelectToken( temp_token, n, grid_x, grid_y, random_tokens): 
            if len(selection_space) == 0 :
                return random_tokens
            selection_space.remove( temp_token )
            temp_token =  random.choice( selection_space)
    return random_tokens 

def tryToSelectToken( token, n, grid_x, grid_y, random_tokens ):
    if token.validMemberOfGame( n, grid_x, grid_y, random_tokens ):
        random_tokens.append( token )
        return True
    else:
        return False    

def __random_token_test():
    assert(  len(selectRandomNTokens( 5, 5, 5 )) == 5 )

def deserialize( token_object ):
    name = token_object[u'name'] 
    return token_dict[name] 

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
    __wallflower_test()
    __church_test()
    __state_test()
    __crowd_test()
    __assassin_test()

    __random_token_test()
