import random

class Distribution(object):
    def __init__( self ):
        self.distribution = {}
        self.cached_distribution = {} 

    def refresh_cached_distribution( self ):
        self.cached_distribution = {}
        last_n = 0
        for category in self.distribution:
            percentage = self.distribution[category]
            next_n = last_n + percentage
            self.cached_distribution[category] = (last_n, next_n)
            last_n = next_n
        return self

    def add_category( self, category_name, category_percentage ):
        self.distribution[category_name] = category_percentage
        return self
   
    def __repr__(self ):
        return str(self.distribution)

    def bounds( self, n ):
        last_n = 0 
        for category in self.distribution:
            percentage = self.distribution[category]
            last_n = int(round(last_n + n * percentage))
            yield (category, last_n)

    def distribute_over( self, n ):
        for i in range( 0 , n ):
            lower_bound = 0             
            for category, upper_bound in self.bounds( n ):
                if i <= upper_bound and i > lower_bound:
                    yield category
                lower_bound = upper_bound 
   
    def normalize( self ):
        """ If the distributions' members don't add up to 1, balance them so that they do. """
        total = 0
        for category in self.distribution:
            total += self.distribution[category]
        for category in self.distribution: 
            #print category + ": " + str(float(self.distribution[category])) + "/" + str(total) + " = " + str(float( self.distribution[category]) / total )
            self.distribution[category] = float(self.distribution[category]) / total
        self.refresh_cached_distribution()

    def generate_random( self ):
        if self.cached_distribution == {}:
            self.refresh_cached_distribution()
        n = random.random()
        for category in self.cached_distribution:
            lower_bound, upper_bound = self.cached_distribution[category]
            if n <= upper_bound and n > lower_bound:
                #print str(upper_bound) + " >= " + str(n) + " > " + str(lower_bound)
                return category
        return "None"

class EqualDistribution( object ):
    def __init__(self):
        self.distribution = [] 
        self.next = 0

    def add_category( self, category ):
        self.distribution.append( category)

    def distribute_over( self, n ):
        for i in range( 0, n ):
            yield self.distribution[self.next]
            self.next = (self.next + 1) % len( self.distribution )

    def generate_random( self ):
        return random.choice( self.distribution )

def no_cleanup( line ):
    return line

def remove_endl( line ):
    return line.strip("\n")

def census_data( line ):
    return line.strip("\"").capitalize()

def load_uniform_distribution( filename, cleanup_function = remove_endl ):
    distribution = EqualDistribution()

    f = open(filename)
    try:
        for line in f:
            distribution.add_category( cleanup_function( line ) )
    finally:
        f.close()

    return distribution


def load_distribution( filename, cleanup_function_key = no_cleanup, cleanup_function_value = remove_endl ):
    distribution = Distribution()

    f = open(filename)
    try:
        for line in f:
            line_array = line.split(',')

            distribution.add_category( cleanup_function_key( line_array[0] ), \
                float(cleanup_function_value( line_array[1])) )
    finally:
        f.close()

    return distribution

def LastNameDistribution():
    LastNameDistribution = load_distribution( "distributions_world/us_surnames.txt", census_data )
    LastNameDistribution.normalize()
    
    return LastNameDistribution

def MaleFirstNameDistribution():
    MaleFirstNameDistribution = load_distribution( "distributions_world/male_forenames", census_data )
    MaleFirstNameDistribution.normalize()
    
    return MaleFirstNameDistribution

def FemaleFirstNameDistribution():
    FemaleFirstNameDistribution = load_distribution( "distributions_world/female_forenames", census_data )
    FemaleFirstNameDistribution.normalize()
    
    return FemaleFirstNameDistribution

def SexDistribution():
    Sex = load_distribution( "distributions_world/sex" )
    Sex.normalize()
    
    return Sex

if __name__ == "__main__":
    LastNameDistribution = LastNameDistribution()
    MaleFirstNameDistribution = MaleFirstNameDistribution()
    FemaleFirstNameDistribution = FemaleFirstNameDistribution()
    Sex = SexDistribution()


    def random_name_by_sex( sex = "Other"):
            if (sex == "Male"):
                return MaleFirstNameDistribution.generate_random() + " " + LastNameDistribution.generate_random()
            elif (sex == "Female"):
                return FemaleFirstNameDistribution.generate_random() + " " + LastNameDistribution.generate_random()
            else:
                return LastNameDistribution.generate_random() + " " + LastNameDistribution.generate_random()

    def random_name():
        sex = Sex.generate_random()
        return random_name_by_sex( sex )

    for i in range( 0, 100):
        print random_name()

