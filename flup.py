# External Libraries
from pymongo import Connection
from bson import ObjectId

# Local Libraries
from state_grid import StateGrid as Grid
import tokens

# Built-in Libraries
import random
import copy

obfuscator = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2",
"3", "4", "5", "6", "7", "8", "9" ]

class Game( object ):
    """ The core game object.
        The game object must be generate()d or load()ed before any further
        operations are performed on it. 
    """
    
    def generate( self, width=10, height=10, gametype="Default", ntokens=8,
                    nturns=10):
        """ Generate a new game and save it to the database. 
            width/height - width & height of the generated grid. 
            gametype - "Clear", "Solution", or "Default" 
            ntokens - the number of different token types to use
            nturns - the number of turns to pre-play in a Default game, OR
                     the number of turns to rewind in a Solution game
        """
        self.width = width
        self.height = height
        self.grid = Grid( width, height )
        self.tokens = tokens.selectRandomNTokens( ntokens )  
        self.nturns = nturns
        self.laziness = 30 #If we've already found 30 solutions, stop looking. 
        self.gamestate = "Playable" # "Playable" || "Unplayable" 
        self.mongo_id = 0 #The mongo_db id of this game record. 
        self.gametype = gametype
        # This isn't valid, but should be overwritten by the 
        # self.selectValidToken() call. 
        self.currentToken = tokens.InvisibleToken() 
        
        print self.tokens
            
        # Initialize Board
        if self.gametype == "Clear":
            self.setup_clear_game()
        elif self.gametype == "Solution":
            self.setup_solution_game()
        else:
            self.setup_default_game()

        self.selectValidToken()
    
    def load( self ):
        mongo_object = self.games_database().find_one({u'_id':
                                        ObjectId(self.mongo_id)} ) 
        self.width = int(mongo_object[u'width'])
        self.height = int(mongo_object[u'height']) 
        self.grid = Grid( self.width, self.height )
        self.tokens = [ tokens.deserialize( token ) for token in
                                mongo_object[u'tokens'] ] 
        self.currentToken = tokens.deserialize( mongo_object[u'currentToken'] )
        self.laziness = mongo_object[u'laziness']
        self.gametype = mongo_object[u'gametype']
        self.gamestate = mongo_object[u'gamestate']
        
        self.grid.unserialize( mongo_object[u'grid'] )
        pass
    
    def save( self):
        """ Save the entirety of the game state to mongodb. """
        document = {"width": self.width, 
                    "height": self.height, 
                    "laziness": self.laziness, 
                    "gamestate": self.gamestate,
                    "gametype": self.gametype,
                    "tokens" : [ token.serialize() for token in self.tokens ],  
                    "currentToken": self.currentToken.serialize(),
                    "grid": self.grid.serialize() }  
        if self.mongo_id == 0:
            self.mongo_id = self.games_database().insert( document )
        else:
            self.games_database().update({'_id':self.mongo_id},{'$set':document}) 

    def games_database( self ):
        connection = Connection()  
        db = connection.flup_database
        return db.games
    
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
        while self.autoplayOneTurn():
            pass
    
    def autoplayOneTurn( self ): 
        """ Completely play one turn for the player. """
        token_point = self.solveOneStep()
        if not token_point:
            print "Solution complete. "
            return False
        token, point = token_point
        if self.grid.placeToken( token, point ):
            return True
        else:
            print "Somehow our valid placement is not valid - ", point
            print self.grid.error
            return self.autoplayOneTurn( )

    def solveOneStep( self, temp_tokens = [] ):
        """ Return the solution to one step of the game, 
            as a tuple (token, point).  """ 
        if temp_tokens == []:
            temp_tokens = copy.deepcopy( self.tokens ) 
        #print "Solving one step with tokens ", temp_tokens 
        test_token = random.choice( temp_tokens )
        #print "Attempting", test_token.name()
        
        valid_placements = self.solveForToken( test_token ) 
        #print "Valid Placements: ", valid_placements
        if len(valid_placements) == 0 and len(temp_tokens) <= 1:
            #print "No valid placements for ", test_token.name()
            return False
        if len(valid_placements) == 0:
            temp_tokens.remove( test_token )
            return self.solveOneStep( temp_tokens )
        return (test_token, random.choice(valid_placements) )
    
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
        # print test_token.name(), place_point
        return ( test_token, place_point ) 
    
    def obfuscateToken( self, token ):
        """ Obfuscate the token using the current set of obfuscation rules. """
        for i in range( 0, len(self.tokens) - 1 ):
            if self.tokens[i].name() == token.name():
                return obfuscator[i] 
    
    def deobfuscateToken( self, fustulated_token ):
        """ Fix the token. """
        for i in range( 0, len(obfuscator) - 1 ):
            if fustulated_token == obfuscator[i]:
                return self.tokens[i]
    
    def attemptMove( self, token, point ):
        self.selectValidToken()
        return self.grid.placeToken( token, point )
    
    def __repr__(self):
        ret = ""
        ret += str(self.grid) + "\n" 
        ret += "\n"
        ret += "Current Token: " + self.currentToken.name() + "\n"
        ret += "\n"
        ret += "Tokens in Play: \n" 
        for token in self.tokens: 
            ret += "\t" + token.name() + "\n" 
        ret += "Game State: " + self.gamestate + "\n" 
        return ret 

def __test_generate_save_and_load():
    g = Game()
    g.generate( 10, 10, "Solution", 10)
    g.save()
    mongo_id = g.mongo_id 
    
    m = Game()
    m.mongo_id = mongo_id
    m.load()
    print m 

def __test_obfuscation():
    g = Game()
    g.generate( 10, 10, "Default", 15)
    obfuscated_token = g.obfuscateToken( tokens.Joker() )
    original_token = g.deobfuscateToken( obfuscated_token ) 
    assert( original_token.name() == tokens.Joker().name() )

if __name__ == '__main__':
    __test_generate_save_and_load() 
    __test_obfuscation()
