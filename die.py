import random

# It's grim, but one has to be precise when describing dice. 
class Die(object):
    
    """ The base class for anything that can be considered a die. """ 
    """ Immutable. """
    def __init__(self):
        self.sides_of_the_die = [1, 2, 3, 4, 5, 6]
    
    def __repr__(self):
        return "Die : " + str( self.sides_of_the_die );

    def roll(self):
        return random.choice( self.sides_of_the_die )

# let's spend some time thinking about randomness. 
# for testing, we want a predetermined set of rolls for each die.
# for gameplay, we want a fixed seed for each die to reduce save-scumming. (or do we?)

