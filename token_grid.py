from grid import Grid
from token_tiles import SingleTokenTile 

class TokenGrid( Grid ):
    def __init__(self, width, height):
        super( TokenGrid, self ).__init__( width, height, SingleTokenTile() )
        self.error = ""

    def placeValidation( self, token, point ):
    """ Determine if token can be placed at point. """
        x, y = point
        if not self.get( x, y ):
            self.error = "Point ", (x,y), " doesn't exist"
            return False
        if self.get(x, y) and self.get( x,y).token:
            self.error = "Point ", (x,y), " already has a token -", self.get(x,y).token.name() 
            return False
        if not token.isValid( self, point ): 
            self.error = "Point ", (x,y), " already contains token: ", token.name()
            return False 
        return True
    
    def placeToken( self, token, point ):
        """ Attempt to place token at point on the grid. Returns True on success and False on failure. """
        x, y = point
        if self.placeValidation( token, point): 
            self.get(x,y).token = token
            token.afterPlacement( self, point )  
            return True
        else:
            return False

    def setToken( self, token, point ):
        """ Like 'placetoken' but without validation or the afterPlacement call. """
        x, y = point
        if not self.get( x, y ):
            return False
        if self.get(x, y) and self.get( x,y).token:
            return False
        self.get(x,y).token = token
        return True

    def clearToken( self, point ):
        """ Remove a token from a point on the grid. """
        x, y = point
        if not self.get( x, y ):
            return False 
        if not self.get( x, y ).token:
            return False
        self.get( x, y ).clear_token() 
        return True

    def frequencyHistogram( self ):
        """ Produce a dictionary of token names and token counts. """
        histogram = {}
        for point in self.points():
            x, y = point
            if self.get( x, y).token:
                name = self.get(x,y).token.name()
                if not name in histogram:
                    histogram[name] = 0
                histogram[name] += 1
        return histogram

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
        if self.get(x, y) and self.get( x, y).token:
            return self.get(x,y).token
        else:
            return False

    def isAnyTokenAtPointInList( self, list_of_points ):
        """ Tests if any token exists at any of these points on the board. """
        for point in list_of_points:
            if self.isAnyTokenAtPoint( point ):
                return True
        return False
