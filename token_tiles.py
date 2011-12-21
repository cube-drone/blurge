from base_tiles import Tile

class SingleTokenTile(Tile):
    """ This tile can have one token on it. """
    def __init__(self):
        super( SingleTokenTile, self).__init__( "." )
        self._token = False

    def get_token( self ):
        return self._token

    def set_token( self, value ):
        if self._token:
            raise TokenOverlap()
        self._token = value

    def clear_token( self, value ):
        self._token = ""

    token = property( get_token, set_token ) 

    def __repr__(self):
        if self.token == "":
            return self.display_character
        else:
            return self.token.__repr__()

    def serialize(self):
        ser = super( SingleTokenTile, self).serialize()
        ser["token"] = self.token
        return ser


class TokenOverlap(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Token overlap!" 
    
