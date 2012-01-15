// The logic for creating a game. Goes with create_game.html

$(document).ready(function() {
    $( "#width" ).slider({
            value:7,
            min: 5,
            max: 12,
            slide: function( event, ui ) { 
                $( "#width_amount" ).val( ui.value );
                }
            });

    $( "#height" ).slider({
            value:7,
            min: 5,
            max: 12,
            slide: function( event, ui ) { 
                $( "#height_amount" ).val( ui.value );
                }
            });
    
    $( "#ntokens" ).slider({
            value:5,
            min: 1,
            max: 10,
            slide: function( event, ui ) { 
                $( "#ntokens_amount" ).val( ui.value );
                }
            });

    $( '#start_game').click( function( event )
    {
        flup.start_game( { 
            width: $( "#width_amount" ).val(),
            height: $( "#height_amount" ).val(),
            ntokens: $( "#ntokens_amount").val(),
            success_callback: function(mongo_id){ window.location = "game.html#" + mongo_id; }
        });
    } 
    );
});

