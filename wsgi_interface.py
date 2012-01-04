from wsgiref.simple_server import make_server, demo_app
import public_interface
import json

master_arguments = {
    'mongo_id': lambda x: str(x),
    'last_move': lambda x: int(x),
    'width': lambda x: int(x),
    'height': lambda x: int(x),
    'gametype': lambda x: str(x),
    'nturns': lambda x: int(x),
    'ntokens': lambda x: int(x),
    'token': lambda x: str(x),
    'point': lambda x: (int(x.split(',')[0]), int(x.split(',')[1]) )
}

def simple_app(environ, start_response):
    """ Functions set to the app come in the format: 
        app:8000/removable/functionName/argumentName=arg/argumentName=arg...
        This app connects to the public_interface.py interface
        But provides HTTP management, JSON conversion, 
        boundary checking, and argument validation. 
    """
    path = environ['PATH_INFO']
    args = path.split("/")
    functionname = args[1]
    string_arguments = filter( lambda x: len( x ) > 0 and x.count('=') > 0, args )
    arguments = {}
    for string_argument in string_arguments: 
        argument, value = string_argument.split("=")
        arguments[argument] = value
    for master_argument, arg_function in master_arguments.iteritems():
        try:
            arguments[master_argument] = arg_function(arguments[master_argument])
        except:
            arguments[master_argument] = ""

    try: 
        if functionname == "start_game":
            response = public_interface.start_game( arguments['width'], 
                                                    arguments['height'],
                                                    arguments['gametype'],
                                                    arguments['ntokens'],
                                                    arguments['nturns'] ) 
        elif functionname == "get_complete_state":
            response = public_interface.get_complete_state( arguments['mongo_id'] )
        elif functionname == "get_update":
            response = public_interface.get_update( arguments['mongo_id'],
                                                    arguments['last_move'] )
        elif functionname == "get_gamestate":
            response = public_interface.get_gamestate( arguments['mongo_id'] )
        elif functionname == "attempt_move":
            response = public_interface.attempt_move( arguments['mongo_id'], 
                                                      arguments['token'], 
                                                      arguments['point'], 
                                                      argumenst['last_move'] )
        else:
            response = False
    except Exception as e:
        response = str(e)
    
    #JSON encode the response.
     
    status = '200 OK'
    response_headers = [('Content-type','application/json')]
    start_response(status, response_headers)
    return [json.dumps( response, indent=4 )]

httpd = make_server('', 8000, simple_app)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()
