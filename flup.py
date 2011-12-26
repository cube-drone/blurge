
from token_grid import TokenGrid
import tokens
import random

class Game( object ):
    def __init__( self, width, height, ntokens):
        self.grid = TokenGrid( width, height )
        self.tokens = tokens.selectRandomNTokens( ntokens )  
        self.laziness = 20
        self.numberOfInitialTokens = 100
        for i in range( 0, self.numberOfInitialTokens ):
            self.placeRandomToken()

    def randomToken( self ):
        return random.choice(self.tokens) 

    def placeRandomToken( self ):
        token = self.randomToken()
        valid_placements = []
        for point in self.grid.points():
            if token.isValid( self.grid, point ):
                valid_placements.append( point ) 
            if len( valid_placements ) > self.laziness:
                break
        if len(valid_placements) == 0:
            return False
        
        if self.grid.placeToken( token, random.choice( valid_placements ) ):
            return True
        else:
            return False


if __name__ == '__main__':
    g = Game( 30, 30, 5)
    print g.grid
