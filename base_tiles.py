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

