
from state_grid import StateGrid as TokenGrid
import tokens
import random
import copy

class Game( object ):
    
    def generate( self, mongo_id ):
        self.grid = TokenGrid( width, height )
        pass

    def generate( self, width, height, gametype, ntokens):
        self.grid = TokenGrid( width, height )
        self.tokens = tokens.selectRandomNTokens( ntokens )  
        self.laziness = 30
        self.numberOfInitialTokens = 100
            
        # Initialize Board
        if gametype == "Clear":
            pass
        elif gametype == "Solution":
            self.completelySolve()
            for i in range(0, 10):
                self.grid.rewindLastFullMove()  
        else: #default gametype
            self.ten_turns_in()

        self.selectValidToken()
    
    def save( self, mongo_id = 0):
        pass
    
    def ten_turns_in( self ):
        for i in range( 0, 10 ):
            self.autoplayOneTurn()

    def selectValidToken( self ):
        result = self.solveOneStep()
        if not result: 
            self.gameOver = True
            return 
        token, point = result
        self.currentToken = token
    
    def completelySolve( self ):
        while  self.autoplayOneTurn( ) :
            pass
    
    def solveForToken( self, token ):
        """ Returns all valid placements for the token. """ 
        valid_placements = [] 
        for point in self.grid.points():
            if token.isValid( self.grid, point) and not self.grid.isAnyTokenAtPoint( point ):
                valid_placements.append( point )
            if len( valid_placements ) > self.laziness:
                break
        return valid_placements

    def solveOneStep( self, temp_tokens = [] ):
        if temp_tokens == []:
            temp_tokens = copy.deepcopy( self.tokens ) 
        test_token = random.choice( temp_tokens )
        
        valid_placements = self.solveForToken( test_token ) 
        if len(valid_placements) == 0 and len(temp_tokens) <= 1:
            return False
        if len(valid_placements) == 0:
            temp_tokens.remove( test_token )
            return self.solveOneStep( temp_tokens )

        place_point = random.choice(valid_placements)
        print test_token.name(), place_point
        return ( test_token, place_point ) 

    def autoplayOneTurn( self ): 
        token_point = self.solveOneStep()
        if not token_point:
            return False
        token, point = token_point
        if self.grid.placeToken( token, point ):
            return True
        else:
            print "Somehow our valid placement is not valid - ", point
            print self.grid.error
            return self.autoplayOneTurn( )
 
    def get_last_delta( self ):
        pass
    
    def get_current_state( self ):
        pass
    
    def attempt_move( self, scrambled_token, point ):
        pass

if __name__ == '__main__':
    g = Game()
    g.generate( 10, 10, "Solution", 10)
    print g.grid
    for counter, move, token, point in g.grid.moves:
        print counter, move, token.name(), point
