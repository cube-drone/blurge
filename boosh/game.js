
var game = {
    mongo_id: "",
    gamestate: "",
    last_move: -1,
    grid_element: ".cube_grid", 
    container_element: ".grid_container",
    next_token_element: ".next_token",
    setup: function( gamestate )
    {
        game.gamestate = gamestate;
        $(game.grid_element).grid( { x:gamestate.width, y:gamestate.height,size: 50, drop_token:game.drop_token } ); 
        $(game.container_element).boxy( ); 
        for( var i = 0; i < gamestate.moves.length; i++ ) 
        {
            game.make_move( gamestate.moves[i] )
        }
        if( gamestate.gamestate != "Playable" )
        {
            alert( "You Win!" );
        }
        game.next_token();
        console.log( game); 
    },
    drop_token: function( token, x, y )
    {
        flup.attempt_move( { 
            mongo_id: game.mongo_id,
            token: token,
            point: x + "-" + y,
            last_move: game.last_move,
            success_callback: game.attempt_move
        });
        console.log( "Drop:", token, x, y )
    },
    attempt_move: function( result )
    {
        if( result === false ) 
        {
            console.log( "Move failed." );
            game.next_token();
        } 
        else
        {
            console.log( "Move successful." );
            console.log( result );
            for( var i = 0; i < result.update.length; i++ ) 
            {
                game.make_move( result.update[i] )
            }
            if( result.playable != "Playable" )
            {
                alert( "You Win!" );
            }
            game.gamestate.currentToken = result.currentToken; 
            game.next_token();
        }
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
        game.last_move = move.sequence;
    },
    next_token: function( )
    {
        var token_element = $(game.next_token_element)
        token_element.html( token_lib.create_token( game.gamestate.currentToken ).draggable({
            revert:'invalid' 
        } )); 
    }

}


$(document).ready(function() {
    game.mongo_id = window.location.href.split("#")[1];
    if( game.mongo_id === undefined ){
        window.location = "index.html";
    }
    
    flup.get_complete_state( { 
        mongo_id: game.mongo_id,
        success_callback: game.setup
    });
});

