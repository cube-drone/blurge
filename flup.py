# External Libraries
from pymongo import Collection

# Local Libraries
from state_grid import StateGrid as Grid
import tokens

# Built-in Libraries
import random
import copy

class Game( object ):
    
    def generate( self, width=10, height=10, gametype="Default", ntokens=8,
                    nturns=10):
        """ Generate a new game and save it to the database. 
            width/height - width & height of the generated grid. 
            gametype - "Clear", "Solution", or "Default" 
            ntokens - the number of different token types to use
            nturns - the number of turns to pre-play in a Default game, OR
                     the number of turns to rewind in a Solution game
        """
        self.grid = Grid( width, height )
        self.tokens = tokens.selectRandomNTokens( ntokens )  
        self.nturns = nturns
        self.laziness = 30 #If we've already found 30 solutions, stop looking. 
        self.gamestate = "Playable" # "Playable" || "Unplayable" 
            
        # Initialize Board
        if gametype == "Clear":
            self.setup_clear_game()
        elif gametype == "Solution":
            self.setup_solution_game()
        else:
            self.setup_default_game()

        self.selectValidToken()
        self.save()
    
    def load( self, mongo_id ):
        self.grid = Grid( width, height )
        pass
    
    def save( self, mongo_id = 0):
        pass
    
    def setup_default_game( self ):
        """ In a Default game, we play n turns for the player. """
        for i in range( 0, self.nturns ):
            self.autoplayOneTurn()
    
    def setup_clear_game( self ):
        """ In a Clear game, we play 0 turns for the player. """
        pass   
 
    def setup_solution_game( self ):
        """ In a Solution game, we solve the game, then rewind n turns. """
        self.completelySolve()
        for i in range(0, self.nturns):
            self.grid.rewindLastFullMove()  
    
    
    def selectValidToken( self ):
        """ Set a verifiably playable token to the current token. """
        result = self.solveOneStep()
        if not result: 
            self.gameState = "Unplayable" 
            return 
        token, point = result
        self.currentToken = token
    
    def completelySolve( self ):
        """ Completely solve the game. (Currently brute-force and non-optimal) """
        while self.autoplayOneTurn( ) :
            pass
    
    def autoplayOneTurn( self ): 
        """ Completely play one turn for the player. """
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

    def solveOneStep( self, temp_tokens = [] ):
        """ Return the solution to one step of the game. """ 
        if temp_tokens == []:
            temp_tokens = copy.deepcopy( self.tokens ) 
        test_token = random.choice( temp_tokens )
        
        valid_placements = self.solveForToken( test_token ) 
        if len(valid_placements) == 0 and len(temp_tokens) <= 1:
            return False
        if len(valid_placements) == 0:
            temp_tokens.remove( test_token )
            return self.solveOneStep( temp_tokens )
    
    def solveForToken( self, token ):
        """ Returns all valid placements for the token. """ 
        valid_placements = [] 
        for point in self.grid.points():
            if token.isValid( self.grid, point) and not self.grid.isAnyTokenAtPoint( point ):
                valid_placements.append( point )
            if len( valid_placements ) > self.laziness:
                break
        return valid_placements

        place_point = random.choice(valid_placements)
        print test_token.name(), place_point
        return ( test_token, place_point ) 

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
