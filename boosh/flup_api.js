// The API for communicating with the Python WSGI server. 

var flup = {
    server_address: "http://"+document.domain+":8000/",
    timeout:5000,  
 
    do_function:function( function_name, args )
    {
        console.log("Flup api: Function " + function_name );
	    console.log("Address: " + flup.server_address );
        var function_complete = false;
        args['function'] = function_name; 

        var success_callback = args.success_callback;
        delete args.success_callback;
        
        var failure_callback = 'failure_callback' in args ? args.failure_callback : function() {
            console.log( function_name + " timed out." ); 
        } 
        delete args.failure_callback;

        var callback_time = 'timeout' in args ? args.timeout : flup.timeout; 
        delete args.timeout;

        var t = setTimeout( function(){
            if( function_complete === true ){ return; };
            function_complete = true;
            console.log("Failure callback: ")
            failure_callback();
        }, callback_time );
 
        $.ajax({
          url: flup.server_address,
          dataType: 'jsonp',
          data: args,
          success: function( data ) {
            if( function_complete === true ){ return; }  
            function_complete = true; 
            success_callback(data);
            }, 
        });       
    },
    
    start_game:function( args )
    /* Args: 'width', 'height', 'ntokens', 'gametype', 'nturns', 'scramble' */
    {
        flup.do_function( 'start_game', args );
    },
   
    get_complete_state:function( args )
    /* Args: 'mongo_id'*/
    { 
        flup.do_function( 'get_complete_state', args );
    },
    
    attempt_move:function( args )
    /* Args: 'mongo_id', 'point', 'last_move' */ 
    {
        flup.do_function( 'attempt_move', args );
    },  
    
    hint: function( args)
    /* Args: 'mongo_id', 'last_move' */
    {
        flup.do_function( 'hint', args );
    },
}


