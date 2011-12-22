from grid import Grid
from token_tiles import SingleTokenTile 

class TokenGrid( Grid ):
    def __init__(self, width, height):
        super( TokenGrid, self ).__init__( width, height, SingleTokenTile() )
    
    def placeToken( self, token, point ):
        """ Attempt to place token at point on the grid. Returns True on success and False on failure. """
        x, y = point
        if not self.get( x, y ):
            return False
        if self.get(x, y) and self.get( x,y).token:
            return False
        if not token.isValid( self, point ): 
            return False 
        
        self.get(x,y).token = token
        token.afterPlacement( self, point )  
        return True
    
    def isTokenAtPoint( self, token, point ): 
        """ Tests if this token exists at a point on the board. """ 
        x, y = point
        if self.get(x, y) and self.get( x, y ).token and self.get( x, y ).token.name() == token.name():
            return True
        else:
            return False

    def isTokenAtPointInList( self, token, list_of_points ):
        """ Tests if this token exists at any of these points on the board. """
        for point in list_of_points:
            if self.isTokenAtPoint( token, point ):
                return True
        return False
    
    def isAnyTokenAtPoint( self, point ):
        """ Tests if ANY token exists at a point on the board. """
        x, y = point
        if self.get(x, y) and self.get( x, y).token and self.get(x, y).token.name() != "InvisibleToken":
            return True
        else:
            return False

    def isAnyTokenAtPointInList( self, list_of_points ):
        """ Tests if any token exists at any of these points on the board. """
        for point in list_of_points:
            if self.isAnyTokenAtPoint( point ):
                return True
        return False

        
