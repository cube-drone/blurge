$(document).ready(function() {

    var Velocity = {};
    
    Velocity.slice_length = 100;
    Velocity.minimum_slice_length = 5;
    Velocity.fiddly_constant = 10;

    Velocity.start_tracking_velocity = function()
    {
        Velocity.x_history = new Array();
        Velocity.y_history = new Array();
        Velocity.timestamp_history = new Array();
        Velocity.counter = 0;
        $(document).bind( 'mousemove', Velocity.velocity_tracker );
    }

    Velocity.stop_tracking_velocity = function()
    {
        $(document).unbind( 'mousemove' );
        Velocity.velocity();
    }

    Velocity.velocity_tracker = function(e)
    {
        Velocity.x_history.push(e.clientX);
        Velocity.y_history.push(e.clientY);
        Velocity.timestamp_history.push( Date.now() );
        Velocity.counter++;
        if ( Velocity.counter % (Velocity.slice_length * 5)  == 0){ Velocity.clean(); }
    }

    Velocity.clean = function()
    {
        Velocity.x_history = Velocity.x_history.slice( 0 - Velocity.slice_length);
        Velocity.y_history = Velocity.y_history.slice( 0 - Velocity.slice_length );
        Velocity.timestamp_history = Velocity.timestamp_history.slice( 0 - Velocity.slice_length );
    }

    Velocity.velocity = function()
    {
        var return_velocity = {};

        Velocity.clean();

        if( Velocity.x_history.length < Velocity.minimum_slice_length ){ return; } 

        for( var i = 0; i < Velocity.x_history.length; i++)
        {
            Velocity.x_history = Velocity.x_history.slice( i - Velocity.slice_length );
            Velocity.y_history = Velocity.y_history.slice( i - Velocity.slice_length );
            var direction = Velocity.try_to_fit_a_direction();
            if ( ! direction === false )
            {
                return_velocity.direction = direction;
                return_velocity.distance = Velocity.hypotamoose( direction.x_delta, direction.y_delta );
                console.log( return_velocity.direction );
                console.log( return_velocity.distance );
                break;
            }
        }

        if( return_velocity.direction == false ) { return; } 

        // Find speed


        return return_velocity;
    }

    Velocity.try_to_fit_a_direction = function()
    {
        var points_x = Velocity.x_history;
        var points_y = Velocity.y_history;

        if( points_x.length < Velocity.minimum_slice_length){ return false; } 

        var x_end = points_x.pop();
        var x_start = points_x.shift();
        var y_end = points_y.pop();
        var y_start = points_y.shift();

        for( var i = 0; i < points_x.length; i++ )
        {
            var x_middle = points_x[i];
            var y_middle = points_y[i];
            if( Velocity.distance_between_point_and_line( x_middle, y_middle, x_start, y_start, x_end, y_end) > Velocity.fiddly_constant )
            {
                return false;
            }
        }

        var direction = {};
        direction.x_delta = (x_start - x_end);
        direction.y_delta = (y_start - y_end);

        return direction;
    }

    Velocity.distance_between_point_and_line = function( point_x, point_y, line_x1, line_y1, line_x2, line_y2)
    {
        var A = point_x - line_x1;
        var B = point_y - line_y1;
        var C = line_x2 - line_x1;
        var D = line_y2 - line_y1;
        var distance_between_point_and_line = Math.abs( A * D - C * B) / Math.sqrt( C * C + D * D );
        /*
        console.log( "Point X: " + point_x);
        console.log( "Point Y: " + point_y);
        console.log( "Line X1: " + line_x1);
        console.log( "Line Y1: " + line_y1);
        console.log( "Line X2: " + line_x2);
        console.log( "Line Y2: " + line_y2);
        console.log( "Distance: " + distance_between_point_and_line );
        console.log( " ");
        */
        return distance_between_point_and_line;
    }

    Velocity.hypotamoose = function( x_delta, y_delta )
    {
        return Math.floor(Math.sqrt( (x_delta * x_delta) + (y_delta * y_delta) ));
    }

    $(document).mousedown( Velocity.start_tracking_velocity );
    $(document).mouseup( Velocity.stop_tracking_velocity );

});
