(function( $ ){

  var methods = {
    init : function( options ) { 
        // options.x is the number of horizontal squares in the cube grid. 
        // options.y is the number of vertical squares in the cube grid. 
        // options.size is the size of cubes in the grid. 
        var x = options.x;
        var y = options.y;
        var size = options.size; 

        var cube_grid = "";

        var total_height = y * size;
        var total_width = x * size; 

        cube_grid += "<div style='position: absolute; top:0; width:"+total_width+"px; height:"+total_height+"px;' >";
        cube_grid += "<table>";

        var counter = 0;
        for( var i = 0; i < x; i++ ) 
        {
            cube_grid += "<tr>";
            for( var j = 0; j < y; j++)
            {
                var background_color = counter % 2 == 0 ? 'blue' : 'pink';
                cube_grid += "<td style='height:"+size+"px; width:"+size+"px; background-color:"+background_color+";' ></td>";
                counter ++;
            }
            cube_grid += "</tr>";
            counter ++;
        }
        cube_grid += "</table>";
        
        this.css('position', 'relative');
        this.append( cube_grid );
    },
    get : function(x, y) {
    }
  };

  // Verbatim from http://docs.jquery.com/Plugins/Authoring
  $.fn.grid = function( method ) {
    
    // Method calling logic
    if ( methods[method] ) {
      return methods[ method ].apply( this, Array.prototype.slice.call(
arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.grid' );
    }    
  
  };

})( jQuery );


