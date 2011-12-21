from base_tiles import *

class ZeroTile(Tile):
    """ A tile that doesn't exist at all. """ 
    def __init__(self):
        super( ZeroTile, self ).__init__( "." )

ZeroTile = ZeroTile()

class Grass(TokenTile):
    def __init__(self):
        super( Grass, self ).__init__( "G" )

class Concrete(TokenTile):
    def __init__(self):
        super( Concrete, self ).__init__( "C" )

class Road(TokenTile, TwoDirectional):
    def __init__(self):
        super( Road, self).__init__("R")

class Office(TokenTile):
    def __init__(self):
        super( Office, self).__init__("O")

# TODO: Define walls as tile edges, not as tiles in-and-of-themselves. 

class Wall(TwoDirectional):
    def __init__(self):
        super( Wall, self).__init__("|")

    def __repr__(self):
        if self.get_direction() == "NS":
            return "|"
        else: 
            return "-"

class WallCorner( FourDirectional ):
    def __init__(self):
        super( WallCorner, self).__init__("*")
