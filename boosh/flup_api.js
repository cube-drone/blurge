// The API for communicating with the Python WSGI server. 

var flup = {
    server_address:"http://192.168.182.131:8000/",
    
    start_game:function( args )
    /* Args: 'width', 'height', 'ntokens', 'gametype', 'nturns', 'success_callback'  */
    {
	args['function'] = 'start_game'; 

        var success_callback = args.success_callback;
	delete args.success_callback;
	$.ajax({
	  url: flup.server_address,
	  dataType: 'jsonp',
	  data: args,
	  success: success_callback, 
	});       
        
    } 
}


