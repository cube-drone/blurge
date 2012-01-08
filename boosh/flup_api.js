var flup = {
    server_address:"http://192.168.182.131:8000/",

    create_url:function( function_name, args )
    {
        url = flup.server_address;
        url = url + function_name + "/"
        for( var key in args )
        {
            url = url + key + "=" + args[key] + "/"
        }
        return url
    },

    start_game:function( args )
    {
        var function_name = "start_game" 
        var function_args = {}
        function_args.width = 'width' in args ? args.width : 10;
        function_args.height = 'height' in args ? args.height : 10;
        function_args.ntokens = 'ntokens' in args ? args.ntokens : 5;
        function_args.gametype = 'gametype' in args ? args.gametype : 'Default';
        function_args.nturns = 'nturns' in args ? args.nturns : 5;
        if( !'success_callback' in args)
        {
            return;
        }
        var success_callback = args.success_callback;
        var failure_callback = 'failure_callback' in args ? args.failure_callback : function()
        { 
            alert("Game creation failed.");  
        };

        var service_url = flup.create_url( function_name, function_args);
        
        $.getJSON(service_url, function(data) {
            alert( "HURP: " + data );
            console.log( data );
        });
        
    } 
}


