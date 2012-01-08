// The API for communicating with the Python WSGI server. 

var flup = {
    server_address:"http://192.168.182.131:8000/",
    
    do_function:function( function_name, args )
    {
        args['function'] = function_name; 

        var success_callback = args.success_callback;
        delete args.success_callback;
        $.ajax({
          url: flup.server_address,
          dataType: 'jsonp',
          data: args,
          success: success_callback, 
        });       
    },
    
    start_game:function( args )
    /* Args: 'width', 'height', 'ntokens', 'gametype', 'nturns', 'success_callback'  */
    {
        flup.do_function( 'start_game', args )
    },
   
    get_complete_state:function( args )
    /* Args: 'mongo_id', 'success_callback' */
    { 
        flup.do_function( 'get_complete_state', args )
    }
 
}


