

(function( $ ){

  var methods = {
    init : function( input_element ) { 
        // this is an input dealing with numercal data from 0 to 99  
        var awesome = $("<div style='position: absolute; height: 100px; width:10px;padding:50px 0px;'> </div>" );
        awesome.append( $("<div class='inner_ticker'></div>") );
        awesome.append( $("<div class='outer_ticker'></div>") );
        this.data( 'input_element', input_element );
        this.append( awesome );
        
        this.rotating_ticker('update');    
    },
    update: function() {
        console.log( $(this.data('input_element')[0] ) ); 
        this.rotating_ticker('set', $(this.data('input_element')[0]).value );
    },
    set: function( new_value ) {
        if (new_value === undefined)
        {
            new_value = "11";
        }
        console.log( "Failure counter: " + new_value );
        var string_val = "00"+ parseInt(new_value, 10).toString();
        var last_two_characters = string_val.substring( string_val.length - 2 );
        var first_character = last_two_characters[0];
        var last_character = last_two_characters[1];
        this.rotating_ticker( 'setInnerRotation', first_character );
        this.rotating_ticker( 'setOuterRotation', last_character );
    },
    setInnerRotation: function( inner )
    {
        var n = parseInt( inner, 10 );
        var rotation = 360 - (n*36);
        this.find( ".inner_ticker").animate ( { rotate: rotation } );
   },
    setOuterRotation: function( outer )
    {
        var n = parseInt( outer, 10 );
        var rotation = (n-1)*36;
        this.find( ".outer_ticker").animate ( { rotate: rotation } );
    }
  };

  // Verbatim from http://docs.jquery.com/Plugins/Authoring
  $.fn.rotating_ticker = function( method ) {
    
    // Method calling logic
    if ( methods[method] ) {
      return methods[ method ].apply( this, Array.prototype.slice.call(
arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.rotating_ticker' );
    }    
  
  };

})( jQuery );


