from json import JSONEncoder

class Serializer(JSONEncoder):
    def __init__( self ):
        super( Serializer, self ).__init__( indent=4 ) 
    def default( self, obj ):
        try:
            return obj.serialize()
        except AttributeError:
            try:
                return JSONEncoder.default( self, obj )
            except TypeError:
                return obj.__repr__()
