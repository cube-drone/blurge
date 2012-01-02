from token_grid import TokenGrid
from moves import serialize_move, unserialize_move 

class StateGrid( TokenGrid ):
    def __init__(self, width, height):
        super( StateGrid, self ).__init__( width, height )
        self.moves = []
        self.movecounter = 0
    
    def placeToken( self, token, point):
        self.moves.append( (self.movecounter, u"placeToken", token, point ) )
        self.movecounter += 1
        if super( StateGrid, self ).placeToken( token, point ):
            return True
        else:
            self.moves.pop()
            self.movecounter -= 1
            return False
    
    def unplaceToken( self, point ):
        super( StateGrid, self ).clearToken( point )
    
    def setToken( self, token, point):
        if super( StateGrid, self ).setToken( token, point ):
            self.moves.append( (self.movecounter, u"setToken", token, point ) ) 
            self.movecounter += 1
            return True
        else:
            return False
    
    def unsetToken( self, point ):
        super( StateGrid, self ).clearToken( point )
    
    def clearToken( self, point):
        token = self.isAnyTokenAtPoint( point )
        if super( StateGrid, self ).clearToken( point ):
            if token:
                self.moves.append( (self.movecounter, u"clearToken", token ,point ) )
                self.movecounter += 1
    
    def unclearToken( self, token, point):
        if not token:
            return True
        super( StateGrid, self ).setToken( token, point )
    
    def rewindLastFullMove( self ):
        """ Only a 'placetoken' counts as a full user move. 
            setToken and clearToken happen as a result of a placetoken. """ 
        
        while len(self.moves) > 0:
            movecounter, movename, token, point = self.moves[ len(self.moves)-1 ] 
            if( movename != 'placeToken' and movename != u'placeToken' ):
                self.rewindLastMove()
            else:
                self.rewindLastMove()
                break
    
    def rewindLastMove( self ):
        if len(self.moves) <= 0:
            return 
        self.rewindMove( self.moves.pop() )
        pass
    
    def rewindMove( self, move ):
        movecounter, movename, token, point = move
        if movename == 'placeToken' or movename == u'placeToken':
            self.unplaceToken( point )
        if movename == 'setToken' or movename == u'setToken':
            self.unsetToken( point )
        if movename == 'clearToken' or movename == u'clearToken':
            self.unclearToken( token, point )
    
    def applyMove( self, move ):
        movecounter, movename, token, point = move
        if movename == 'placeToken' or movename == u'placeToken':
            self.setToken( token, point )
        if movename == 'setToken' or movename == u'setToken':
            self.setToken( token, point ) 
        if movename == 'clearToken' or movename == u'clearToken':
            self.clearToken( point ) 
    
    def serialize( self ):
        return [ serialize_move( move ) for move in self.moves ] 
    
    def unserialize( self, moves ):
        for move in moves: 
            self.applyMove( unserialize_move( move ) )
