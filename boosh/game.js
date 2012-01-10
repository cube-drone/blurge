
var game = {
    grid_element: ".cube_grid", 
    container_element: ".grid_container",
    next_token_element: ".next_token",
    setup: function( gamestate )
    {
        console.log( gamestate); 
        $(game.grid_element).grid( { x:gamestate.width, y:gamestate.height,size: 50, drop_token:game.drop_token } ); 
        $(game.container_element).boxy( ); 
        for( var i = 0; i < gamestate.moves.length; i++ ) 
        {
            game.make_move( gamestate.moves[i] )
        }
        if( gamestate.gamestate != "Playable" )
        {
            console.log( "Unplayable!" );
        }
        game.next_token( gamestate.currentToken );
    },
    drop_token: function( token, x, y )
    {
        console.log( "Drop:", token, x, y )
    },
    make_move: function( move )
    {
        move =  move_lib.move_to_object(move);
        if( move.movename === "setToken" || move.movename === "placeToken" ){
            $(game.grid_element).grid( 'place', move.x, move.y, token_lib.create_token( move.token ) );  
            // render this space unusable
            $(game.grid_element).grid( 'get', move.x, move.y).droppable('option', 'disabled', true )
        }
        else if( move.movename === "clearToken")
        {
            $(game.grid_element).grid( 'clear', move.x, move.y );  
            // this space becomes usable again. 
            $(game.grid_element).grid( 'get', move.x, move.y).droppable('option', 'disabled', false )
        } 
    },
    next_token: function( token )
    {
        var token_element = $(game.next_token_element)
        token_element.html( token_lib.create_token( token ).draggable({
            revert:'invalid' 
        } )); 
    }

}


$(document).ready(function() {
    mongo_id = window.location.href.split("#")[1];
    if( mongo_id === undefined ){
        window.location = "index.html";
    }
    
    flup.get_complete_state( { 
        mongo_id: mongo_id,
        success_callback: game.setup
    });
});

