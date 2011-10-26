import errors

class Tile(object):
    """ The base class for anything that can be considered a tile. """ 
    """ Immutable. """
    def __init__(self, display_character):
        self.display_character = display_character
    
    def __repr__(self):
        return self.display_character

    def serialize(self):
        return {
                "type": self.__class__.__name__,
                "display": self.__repr__(),
                }


class TokenTile(Tile):
    """ This tile can have tokens on it. """
    def __init__(self, display_character):
        super( TokenTile, self ).__init__( display_character )
        self.tokens = []

    def put_token(self, token):
        self.tokens.append( token )
        return self

    def serialize(self):
        ser = super( TokenTile, self).serialize()
        ser["tokens"] = self.tokens
        return ser

class FourDirectional(Tile):
    """ Defines a tile that can be facing N, S, W, or E. """ 
    def __init__(self, display_character, ):
        super( FourDirectional, self ).__init__( display_character )
        self.direction = "N"

    def set_direction( self, direction ):
        if direction != "N" \
            and direction != "E" \
            and direction != "S" \
            and direction != "W":
            raise Hell( "You can't pass a direction that is not 'N', 'E', 'S', or 'W' to a directional tile." ) 
        self.direction = direction
        return self

    def rotate(self):
        if self.direction == "N":
            self.direction = "E"
        elif self.direction == "E":
            self.direction = "S"
        elif self.direction == "S":
            self.direction = "W"
        elif self.direction == "W":
            self.direction = "N"
        return self

    def get_direction(self):
        return self.direction

    def get_rotation(self ):
        if self.direction == "N":
            return 0
        if self.direction == "E":
            return 90
        if self.direction == "S":
            return 180
        if self.direction == "W":
            return 270
    
    def serialize(self):
        ser = super( FourDirectional, self).serialize()
        ser["direction"] = self.get_direction()
        ser["rotation"] = self.get_rotation()
        return ser

class TwoDirectional(FourDirectional):
    """ Defines a tile that can only be facing NS or WE. """
    def __init__(self, display_character):
        super( TwoDirectional, self ).__init__( display_character )
        self.direction = "NS"

    def set_direction(self, direction ):
        if direction != "NS" \
            and direction != "SN" \
            and direction != "EW" \
            and direction != "WE":
            raise Hell( "You can't pass a direction that is not 'NS',or 'WE' to a two-directional tile." ) 
        if direction == "SN":
            self.direction = "NS"
        elif direction == "EW":
            self.direction = "WE"
        else: 
            self.direction = direction
        return self

    def rotate(self):
        if self.direction == "NS":
            self.direction = "WE"
        elif self.direction == "WE":
            self.direction = "NS"
        return self

    def get_rotation(self):
        if self.direction == "NS":
            return 0
        if self.direction == "WE":
            return 90

