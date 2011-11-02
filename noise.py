import random
import grid
import math

def line_noise( line, name_of_property, randomness_factor ):
    """ 
    One-Dimensional Midpoint Displacement, as described here: 
    http://www.gameprogrammer.com/fractal.html

    With the difference that we start with a list containing
    a discrete set of objects (line), and on each object we
    set a property (name_of_property).

    Each midpoint object is set to the average of the points
    at each edge multiplied by the 'randomness factor'. A high
    randomness factor ( 0.8 - 1 ) will produce a jagged, noisy
    line. A low randomness factor ( 0 - 0.3 ) will produce
    a smooth, creamy line. 

    This also makes its modifications directly to the line in question.
    """
    __line_noise_from_start_to_end( line, name_of_property, randomness_factor, 0, len(line)-1 )

def grid_noise( grid, name_of_property, randomness_factor ):
    """
    The diamond-square algorithm, as described here: 
    http://www.gameprogrammer.com/fractal.html

    Very similar to line noise, except that we are doing it on a two
    dimensional plane (as described in grid.py) instead of a three
    dimensional one. 

    This makes its modifications directly to the grid in question. 
    """
    
    __grid_noise_from_corners( grid, name_of_property, randomness_factor, 0, grid.width-1, 0, grid.height-1 )

class NoiseChoice(object):
    """
    An object that, given a 'noise' value, can be used to make a choice 
    between a variety of different things.
    """
    def __init__(self, list_of_choices=[], midpoint = 0.5):
        self.list_of_choices = list_of_choices
        self.noise = midpoint
    def choice(self): 
        return self.list_of_choices[int(round(self.noise * len(self.list_of_choices)))]

def __line_noise_from_start_to_end( list_of_objects, name_of_property, randomness_factor, start, end ):
    
    middle_index = __middle( start, end );

    if middle_index == 0:
        return 
    
    # Get boundary values
    left_val = getattr( list_of_objects[start], name_of_property)
    right_val = getattr( list_of_objects[end], name_of_property) 
  
    # Generate center value
    middle_val = __average_and_randomize( randomness_factor, left_val, right_val )
    setattr( list_of_objects[middle_index], name_of_property, middle_val )
    
    # And now the recursive part! 
    __line_noise_from_start_to_end( list_of_objects, name_of_property, randomness_factor, start, middle_index )
    __line_noise_from_start_to_end( list_of_objects, name_of_property, randomness_factor, middle_index, end )

def __grid_noise_from_corners( grid, name_of_property, randomness_factor, start_x, end_x, start_y, end_y ):
    middle_x = __middle( start_x, end_x )
    middle_y = __middle( start_y, end_y )

    # I had to convince myself that this is right. If there is no middle value for x OR y, then all
    #  of the values are already set, here, I think. 
    if middle_x == 0 or middle_y == 0:
        return

    # Here we fetch all of the tiles that are of importance to the current procedure. 
    corner_bottom_left = grid.get( start_x, start_y )
    corner_top_left = grid.get( start_x, end_y )
    corner_bottom_right = grid.get( end_x, start_y )
    corner_top_right = grid.get( end_x, end_y )

    middle_tile = grid.get( middle_x, middle_y )


    corner_bottom_left_val = getattr( corner_bottom_left, name_of_property )
    corner_top_left_val = getattr( corner_top_left, name_of_property )
    corner_bottom_right_val = getattr( corner_bottom_right, name_of_property )
    corner_top_right_val = getattr( corner_top_right, name_of_property )

    middle_val = __average_and_randomize( randomness_factor, \
                                                corner_bottom_left_val, \
                                                corner_top_left_val, \
                                                corner_bottom_right_val, \
                                                corner_top_right_val )

    setattr( middle_tile, name_of_property, middle_val ) 
    
    # these stray beyond the boundaries of our square
    left_post_x = start_x - middle_x
    right_post_x = end_x + middle_x
    bottom_post_y = start_y - middle_y
    top_post_y = end_y + middle_y

    if left_post_x < 0:
        left_post_x = 0
    if right_post_x > grid.width - 1:
        right_post_x = grid.width - 1
    if bottom_post_y < 0:
        bottom_post_y = 0
    if top_post_y > grid.height - 1:
        top_post_y = grid.height - 1

    left_post = grid.get( left_post_x, middle_y ) 
    left = grid.get( start_x, middle_y )
    right_post = grid.get( right_post_x, middle_y )
    right = grid.get( end_x, middle_y )
    top_post = grid.get( middle_x, top_post_y )
    top = grid.get( middle_x, start_y )
    bottom_post = grid.get( middle_x, bottom_post_y )
    bottom = grid.get( middle_x, end_y )

    left_post_val = getattr( left_post, name_of_property )
    right_post_val = getattr( right_post, name_of_property ) 
    top_post_val = getattr( top_post, name_of_property ) 
    bottom_post_val = getattr( bottom_post, name_of_property )

    left_val = __average_and_randomize( randomness_factor, \
                                                corner_top_left_val, \
                                                corner_bottom_left_val, \
                                                middle_val, \
                                                left_post_val )
    right_val = __average_and_randomize( randomness_factor, \
                                                corner_top_right_val, \
                                                corner_bottom_right_val, \
                                                middle_val, \
                                                right_post_val )
    top_val = __average_and_randomize( randomness_factor, \
                                                corner_top_right_val, \
                                                corner_top_left_val, \
                                                middle_val, \
                                                top_post_val ) 
    bottom_val = __average_and_randomize( randomness_factor, \
                                                corner_bottom_right_val, \
                                                corner_bottom_left_val, \
                                                middle_val, \
                                                bottom_post_val )

    setattr( left, name_of_property, left_val )
    setattr( right, name_of_property, right_val )
    setattr( top, name_of_property, top_val )
    setattr( bottom, name_of_property, bottom_val )


    __grid_noise_from_corners( grid, name_of_property, randomness_factor, start_x, middle_x, start_y, middle_y )
    __grid_noise_from_corners( grid, name_of_property, randomness_factor, middle_x, end_x, start_y, middle_y )
    __grid_noise_from_corners( grid, name_of_property, randomness_factor, start_x, middle_x, middle_y, end_y )
    __grid_noise_from_corners( grid, name_of_property, randomness_factor, middle_x, end_x, middle_y, end_y )

def __middle( start, end ): 
    """
    Calculate the (integer) value between start and end.
    
    Returns 0 for most invalid inputs. 
    """
    if start == end: 
        return 0
    if start - end == 1:
        return 0
    middle = int( start + round((end - start) / 2) )
    if middle == start or middle == end:
        return 0

    return middle

def __average_and_randomize( randomness_factor, *args ):
    """ Take all of the arguments, average them,
        then multiply by a random value, muted by the randomness factor.

        This assumes that all args will be between 0 and 1, and
        will not produce values lower than 0 or higher than 1. 
    """ 
    average = sum( args ) / len( args )
    randomness = (random.random() - 0.5) * randomness_factor
    averaged_and_randomized = average + randomness 
    
    if averaged_and_randomized <= 0:
        return 0
    if averaged_and_randomized >= 1:
        return 1

    return averaged_and_randomized


class __test_mock_object:
    def __init__(self):
        self.sassiness = 0.5

def __test_line_noise():
    # Testing.

    TOTAL_NUMBER_OF_VALUES = 10000

    list_of_objects =  [ __test_mock_object() for o in range( 0, TOTAL_NUMBER_OF_VALUES ) ]
    line_noise( list_of_objects, "sassiness", 0.5  )
    
    frequency_map = {}

    for i in range(0, 11):
        frequency_map[i] = 0

    for o in list_of_objects:
        sassy_factor = int(round(o.sassiness*10))
        assert (not o.sassiness > 1)
        assert (not o.sassiness < 0)
        frequency_map[sassy_factor] += 1 

    for i in range(0, 10):
        number_of_values_in_range = frequency_map[i]
        assert(not number_of_values_in_range == 0)
        assert(not number_of_values_in_range == TOTAL_NUMBER_OF_VALUES)
    print "Line Noise Passed!" 

def __test_grid_noise():
    # Testing.

    HEIGHT = 100
    WIDTH = 500
    TOTAL_NUMBER_OF_VALUES = HEIGHT * WIDTH

    g = grid.Grid( HEIGHT, WIDTH, __test_mock_object() )

    grid_noise( g , "sassiness", 0.5  )
    
    frequency_map = {}

    for i in range(0, 11):
        frequency_map[i] = 0

    for o in g.all():
        sassy_factor = int(round(o.sassiness*10))
        assert (not o.sassiness > 1)
        assert (not o.sassiness < 0)
        frequency_map[sassy_factor] += 1 

    for i in range(0, 10):
        number_of_values_in_range = frequency_map[i]
        assert(not number_of_values_in_range == 0)
        assert(not number_of_values_in_range == TOTAL_NUMBER_OF_VALUES)
    print "Grid Noise Passed!" 

def __test_middle():
    assert( __middle( 0, 10) == 5 ) 
    assert( __middle( 2, 4) == 3 )
    assert( __middle( 3, 4) == 0 )
    assert( __middle( 3, 3) == 0 )
    assert( __middle( 3, 0) == 1 )
    print "Middle Passed!" 


def __test_average_and_randomize():
    assert __average_and_randomize( 0, 0.5, 0.5, 0.5, 0.5 ) == 0.5
    assert __average_and_randomize( 0, 0.25, 0.75, 0.25, 0.75) == 0.5
    assert not __average_and_randomize( 1, 0.5, 0.5, 0.5, 0.5 ) == 0.5
    assert __average_and_randomize( 0, 2, 2, 2) == 1
    assert __average_and_randomize( 0, -2, -2, -2) == 0

    print "Average and Randomize Passed!" 


if __name__ == "__main__":

    __test_average_and_randomize()
    __test_middle()
    __test_line_noise()
    __test_grid_noise()

    print "Tests Passed!" 
