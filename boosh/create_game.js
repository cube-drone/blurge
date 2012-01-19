// The logic for creating a game. Goes with create_game.html

$(document).ready(function() {
    $( "#width" ).slider({
            value: $( "#width_amount").val(),
            min: 5,
            max: 12,
            slide: function( event, ui ) { 
                $( "#width_amount" ).val( ui.value );
                }
            });

    $( "#height" ).slider({
            value: $( "#height_amount").val(),
            min: 5,
            max: 12,
            slide: function( event, ui ) { 
                $( "#height_amount" ).val( ui.value );
                }
            });
    
    $( "#ntokens" ).slider({
            value: $("ntokens_amount").val(),
            min: 1,
            max: 10,
            slide: function( event, ui ) { 
                $( "#ntokens_amount" ).val( ui.value );
                }
            });
    
    $( "#scramble" ).slider({
            value:0,
            min: 0,
            max: 1,
            slide: function( event, ui ) { 
                if(ui.value === 0)
                { 
                    $( "#scramble_amount" ).val( "Easy" ).data('scramble', false);
                }
                else
                {
                    $( "#scramble_amount" ).val( "Hard" ).data('scramble', true);
                }
                }
            });

    $( '#start_game').click( function( event )
    {
        flup.start_game( { 
            width: $( "#width_amount" ).val(),
            height: $( "#height_amount" ).val(),
            ntokens: $( "#ntokens_amount").val(),
            scramble: $( "#scramble_amount").data('scramble'), 
            //success_callback: function(mongo_id){ console.log( mongo_id); } 
            success_callback: function(mongo_id){ window.location = "game.html#" + mongo_id; }
        });
    } 
    );
});

