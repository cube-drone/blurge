from token_grid import TokenGrid

class StateGrid( TokenGrid ):
    def __init__(self, width, height):
        super( StateGrid, self ).__init__( width, height )
        self.moves = []
        self.movecounter = 0
    
    def placeToken( self, token, point):
        self.moves.append( (self.movecounter, "placeToken", token, point ) )
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
            self.moves.append( (self.movecounter, "setToken", token, point ) ) 
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
                self.moves.append( (self.movecounter, "clearToken", token ,point ) )
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
            if( movename != 'placeToken' ):
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
        if movename == 'placeToken':
            self.unplaceToken( point )
        if movename == 'setToken':
            self.unsetToken( point )
        if movename == 'clearToken':
            self.unclearToken( token, point )
    
    def applyMove( self, move ):
        movecounter, movename, token, point = move
        if movename == 'placeToken':
            self.setToken( token, point )
        if movename == 'setToken':
            self.setToken( token, point ) 
        if movename == 'clearToken':
            self.clearToken( point ) 
    
    def serialize( self ):
        return self.moves
    def unserialize( self, moves ):
        pass
    def client_serialize( self ):
        pass

