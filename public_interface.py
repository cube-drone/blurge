from flup import Game
from moves import obfuscate_move 

def start_game( width=10, height=10, gametype="Default", ntokens=8, nturns=10,
                scramble=False): 
    print "=== Start Game === " 
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
    if scramble == None:
        scramble = False
    g = Game()
    g.generate( width, height, gametype, ntokens, nturns, scramble)
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
    print "=== Get Complete State ==="
    g = load_game( mongo_id ) 
    return_object = { 
        u'width': g.width,
        u'height': g.height, 
        #u'tokens': [ token.name() for token in g.tokens ],
       
        u'success': True, 
        u'update': [ obfuscate_move( move, g) for move in g.grid.moves ],
        u'failureCounter': g.failureCounter, 
        u'playable': g.gamestate,
        u'currentToken': g.obfuscateToken( g.currentToken ),
    }
    if not g.scramble:
         return_object[u'tokens'] = [ token.name() for token in g.tokens ] 
    return return_object 

def get_update( mongo_id, last_move ):
    print "=== Get Update ==="
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
    print "=== Get Gamestate ===" 
    g = load_game( mongo_id )
    return g.gamestate

def attempt_move( mongo_id, point, last_move ):
    print "=== Attempt Move ===" 
    if point == None:
        raise Exception( "point is required" )
    if last_move == None:
        last_move = -1

    g = load_game( mongo_id )
    print "Attempting To Play  ", g.currentToken.name(), " at ", point

    if g.attemptMove( point, last_move ):
        g.save()
        return { u'success': True, 
                 u'update': __update( g, last_move ), 
                 u'failureCounter': g.failureCounter ,
                 u'playable': g.gamestate, 
                 u'currentToken': g.obfuscateToken( g.currentToken ) } 
    else:
        g.save()
        return { u'success': False,
                 u'playable': g.gamestate,
                 u'failureCounter': g.failureCounter }

def hint( mongo_id, last_move ):
    print "=== Hint ===" 
    if last_move == None:
        last_move = -1
    g = load_game( mongo_id )
    g.hint( last_move )
    g.save()
    return { u'success': True, 
             u'update': __update( g, last_move ), 
             u'failureCounter': g.failureCounter,
             u'playable': g.gamestate, 
             u'currentToken': g.obfuscateToken( g.currentToken ) } 

if __name__ == '__main__':
    mongo_id = start_game()
    state = get_complete_state(mongo_id)
    update = get_update( mongo_id, -1 )
    gamestate = get_gamestate( mongo_id )
    print "Gamestate: ", state 
    print gamestate
    
    lastmove = update[ len( update ) -1 ] 
    counter, blah, blor, blop = lastmove
    
    g = load_game( mongo_id )
    token, point = g.solveOneStep([g.deobfuscateToken(state[u'currentToken'])])
    print "Attempting to play ", token.name(), " at point ", point  
    print 
    print attempt_move( mongo_id, g.obfuscateToken( token ), point, counter) 
    print 
    print get_update( mongo_id, counter ) 
