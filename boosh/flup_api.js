// The API for communicating with the Python WSGI server. 

var flup = {
    server_address:"http://192.168.182.131:8000/",
    timeout:3000,  
 
    do_function:function( function_name, args )
    {
        var function_complete = false;
        args['function'] = function_name; 

        var success_callback = args.success_callback;
        delete args.success_callback;
        var failure_callback = 'failure_callback' in args ? args.failure_callback : function() {
            console.log( function_name + " timed out." ); 
        } 

        var t = setTimeout( function(){
            if( function_complete === true ){ return; };
            function_complete = true;
            failure_callback();
        }, flup.timeout );
 
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


