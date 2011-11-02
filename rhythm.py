import random
from errors import Hell
import noise 

class Rhythm(object):
    def __init__(self):
        pass
    def duration_map(self):
        return [4, 4, 4, 4] 

class RandomSplitRhythm(Rhythm):
    def __init__(self, initial_probability, recursive_probability_factor):
        self.initial_probability = initial_probability
        self.recursive_probability_factor = recursive_probability_factor
        
    def __generate(self):
        self.meter = [1]
        self.split_limit = 16
        self.smallest_note = 32

        self.__split( 0, self.initial_probability )
        self.__sanity_check( )

    def __split(self, index, probability):
        if self.split_limit > 0 and self.meter[index] < self.smallest_note and random.random() < probability:
            self.split_limit -= 1
            new_val = self.meter[index] * 2
            self.meter[index] = new_val
            self.meter.insert(index, new_val) 
            self.__split( index + 1, probability * self.recursive_probability_factor ) 
            self.__split( index, probability * self.recursive_probability_factor)

    def __sanity_check( self) :
        val = 0
        for i in self.meter:
            val = val + 1.0/i
        if val != 1.0:
            # yes, I know float equality is touchy business
            raise Hell( "This meter does not add up to a whole meter for some reason." )
    
    def duration_map(self):
        self.__generate()
        return self.meter

def PatternedSplitRhythm(Rhythm):
    def __init__(self, rhythm, number_of_rhythms = 6, length = 3, randomness_factor = 0.5):
        self.rhythm = rhythm
        self.number_of_rhythms = number_of_rhythms
        self.length = length
        self.randomness_factor = randomness_factor

    def duration_map(self):
        rhythms = []
        for i in range(0, self.number_of_rhythms):
            rhythms.append( self.rhythm.duration_map() )
        pass
        
        rhythms = [noise.NoiseChoice(rhythms) for i in range( 0, self.length )]
        noise.line_noise( rhythms, "noise", self.randomness_factor)  

        returnval = []
        for rhythm in rhythms:
            returnval.extend( rhythm.choice() )
        
        return returnval

def __test_random_split_rhythm():
    r = RandomSplitRhythm( 0.9, 0.55 ) 
    print r.duration_map()


if __name__ == "__main__":
    __test_random_split_rhythm()
