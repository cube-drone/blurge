(function( $ ){

  $.fn.boxy = function() {
    var contained_object = this.children()[0] ;
    $(contained_object).draggable( { scroll: true} ) 
    return this; 
  };

})( jQuery );
