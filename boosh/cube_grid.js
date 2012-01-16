(function( $ ){

  var methods = {
    init : function( options ) { 
        // options.x is the number of horizontal squares in the cube grid. 
        // options.y is the number of vertical squares in the cube grid. 
        // options.size is the size of cubes in the grid. 
        // options.drop_token is the function to be called if a user drops a
        //  token on one of the grid items.  
        this.data( 'maxwidth', options.x - 1 )
        this.data( 'maxheight', options.y - 1)
        var x = options.x;
        var y = options.y;
        var size = options.size; 
        var drop_token = options.drop_token;

        var total_height = y * size;
        var total_width = (x+1) * size; 

        var outer_div = $("<div style='position: absolute; top:0;width:"+total_width+"px; height:"+total_height+"px;' ></div>");
        var table = $("<table style='table-layout:fixed;'></table>");

        console.log("Manufacturing grid." );
        for( var j = 0; j < x; j++)
        {
            table.append("<col width='"+size+"px'></col>");
        }
        for( var i = 0; i < y; i++ ) 
        {
            var table_row = $("<tr></tr>");
            for( var j = 0; j < x; j++)
            {
                var odd = (i + j) % 2 == 0 ? 'even' : 'odd';
                var grid_square = $("<td class='x_"+j+" y_"+(y-i-1)+" gridsquare "+odd+"' style='height:"+size+"px; width:"+size+"px; min-height="+size+"px;min-width="+size+"px; overflow=hidden; ' ></td>")
                grid_square.data("x",j).data("y", (y-i-1)) ;
                var click_fn = function( grid_square)
                {
                    var target = grid_square;
                    return function( event, ui )
                    {
                        var x = target.data('x') ;
                        var y = target.data('y') ;
                        drop_token(  x, y );
                    }
                }
                var drop_fn = function( grid_square )
                {
                    var target = grid_square;
                    return function( event, ui )
                    {
                        token = ui.draggable;
                        var x = target.data('x') ;
                        var y = target.data('y') ;
                        drop_token(  x, y );
                        token.remove();
                    }
                }
                grid_square.dblclick( click_fn(grid_square) );
                grid_square.droppable( {
                        accept:".token",
                        activeClass: "drop_target", 
                        hoverClass: "drop_target_hover",
                        drop: drop_fn( grid_square )
                });  
                table_row.append( grid_square );
            }
            table.append(table_row);
        }
        outer_div.append(table);
        
        this.css('position', 'relative');
        this.append( outer_div );
    },
    get: function(x, y) {
        var selector = ".x_"+x+".y_"+y;
        return $(selector);
    },
    place: function(x, y, token){
        this.grid("get", x, y).append( token );
    }, 
    clear: function(x, y){
        this.grid("get", x, y).html("");
    }, 
    maxheight: function(){
        return this.data("maxheight");
    },
    maxwidth: function(){
        return this.data("maxwidth");
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


