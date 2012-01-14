from flup import Game
from moves import obfuscate_move 

def start_game( width=10, height=10, gametype="Default", ntokens=8, nturns=10): 
    if width == None:
        width = 10
    if height == None:
        height = 10
    if gametype == None:
        gametype = "Default"
    if ntokens == None:
        ntokens = 8
    if nturns == None:
        nturns = 10
    g = Game()
    g.generate( width, height, gametype, ntokens, nturns)
    g.save()
    return str(g.mongo_id) 

def load_game( mongo_id ):
    if mongo_id == None:
        raise Exception( "mongo_id is required" )
    g = Game()
    g.mongo_id = mongo_id
    g.load()
    return g

def get_complete_state( mongo_id ): 
    g = load_game( mongo_id ) 
    return_object = { 
        u'width': g.width,
        u'height': g.height, 
        u'moves': [ obfuscate_move( move, g) for move in g.grid.moves ],
        u'currentToken': g.obfuscateToken( g.currentToken ),
        u'tokens': [ g.obfuscateToken( token) for token in g.tokens ], 
        #u'tokens': [ token.name() for token in g.tokens ],
        u'gamestate': g.gamestate
    } 
    return return_object 

def get_update( mongo_id, last_move ):
    if last_move == None:
        last_move = -1
    g = load_game( mongo_id )
    return __update( g, last_move )

def __update( game, last_move ):
    moves = []
    for move in game.grid.moves:
        movecounter, movename, token, point = move
        if movecounter > last_move:
            moves.append(obfuscate_move( move, game ))
    return moves

def get_gamestate( mongo_id ):
    g = load_game( mongo_id )
    return __gamestate( g )

def __gamestate( game ):
    return game.gamestate

def attempt_move( mongo_id, obfuscated_token, point, last_move ):
    if obfuscated_token == None:
        raise Exception( "obfuscated_token is required" )
    if point == None:
        raise Exception( "point is required" )
    if last_move == None:
        last_move = -1

    g = load_game( mongo_id )
    token = g.deobfuscateToken( obfuscated_token )
    print "Attempting To Play  ", token.name(), " at ", point

    if g.currentToken.name() != token.name():
        return False
    if g.attemptMove( token, point ):
        g.save()
        return { u'update': __update( g, last_move ), 
                 u'playable': __gamestate( g ), 
                 u'currentToken': g.obfuscateToken( g.currentToken ) } 
    else:
        return False

def hint( mongo_id, last_move ):
    if last_move == None:
        last_move = -1
    g = load_game( mongo_id )
    token_point = g.solveOneStep([g.currentToken])
    if token_point:
        token, point = token_point
    else:
        g.gamestate = "Unplayable"
        g.save()
        return False;  
    if g.attemptMove( token, point ):
        g.save()
        return { u'update': __update( g, last_move ), 
                 u'playable': __gamestate( g ), 
                 u'currentToken': g.obfuscateToken( g.currentToken ) } 

if __name__ == '__main__':
    mongo_id = start_game()
    state = get_complete_state(mongo_id)
    update = get_update( mongo_id, -1 )
    gamestate = get_gamestate( mongo_id )
    
    lastmove = update[ len( update ) -1 ] 
    counter, blah, blor, blop = lastmove
    
    g = load_game( mongo_id )
    token, point = g.solveOneStep([g.deobfuscateToken(state[u'currentToken'])])
    print "Attempting to play ", token.name(), " at point ", point  
    print 
    print attempt_move( mongo_id, g.obfuscateToken( token ), point, counter) 
    print 
    print get_update( mongo_id, counter ) 
