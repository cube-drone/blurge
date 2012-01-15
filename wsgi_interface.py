from wsgiref.simple_server import make_server, demo_app
import public_interface
import json

master_arguments = {
    'callback': lambda x: str(x),
    'mongo_id': lambda x: str(x),
    'last_move': lambda x: int(x),
    'width': lambda x: int(x),
    'height': lambda x: int(x),
    'gametype': lambda x: str(x),
    'nturns': lambda x: int(x),
    'ntokens': lambda x: int(x),
    'token': lambda x: str(x),
    'point': lambda x: (int(x.split('-')[0]), int(x.split('-')[1]) ),
    'function': lambda x: str(x)
}

def wsgi_error(environ, start_response, error):
    """ Returns an error. """
    status = '400 BAD REQUEST'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    return [ error ] 

def application(environ, start_response):
    """ Functions set to the app come in the format: 
        :8080/?function=start_game&callback=awesome&arg1=blah ... 
        This app connects to the public_interface.py interface
        But provides HTTP management, JSON conversion, 
        boundary checking, and argument validation. 
    """
    path = environ['QUERY_STRING']
    args = path.split("&")
    string_arguments = filter( lambda x: len( x ) > 0 and x.count('=') > 0, args )

    arguments = {}
    for string_argument in string_arguments: 
        argument, value = string_argument.split("=")
        arguments[argument] = value
    for master_argument, arg_function in master_arguments.iteritems():
        try:
            arguments[master_argument] = arg_function(arguments[master_argument])
        except:
            arguments[master_argument] = None

    if arguments['function'] == None or arguments['callback'] == None:
        return wsgi_error( environ, start_response, "Nope dot com. No function or callback provided." )
    functionname = arguments['function']
    
    try: 
        if functionname == "pull":
            import commands
            response = commands.getoutput('bash git_reload &') 
        elif functionname == "start_game":
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
                                                      arguments['point'], 
                                                      arguments['last_move'] )
        elif functionname == "hint":
            response = public_interface.hint( arguments['mongo_id'],
                                                arguments['last_move'] ) 
        else:
            return wsgi_error( environ, start_response, functionname + " isn't an available functon" )

    except Exception as e:
        print "OH NO! EXCEPTION!", e.__repr__()
        response = e.__repr__()
    
    #JSON encode the response.
    print functionname, ":" 
    print arguments
    print "------------------------"
 
    status = '200 OK'
    response_headers = [('Content-type','application/json')]
    start_response(status, response_headers)
    print response
    print 
    print
    return [ arguments['callback'] + "(" + json.dumps( response, indent=4 )+")" ]

if __name__ == "__main__":
    httpd = make_server('', 8000, application)
    print "Serving HTTP on port 8000..."
    
    # Respond to requests until process is killed
    httpd.serve_forever()
