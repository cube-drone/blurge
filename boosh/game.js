
var game = {
    mongo_id: "",
    gamestate: "",
    last_move: -1,
    grid_element: ".cube_grid", 
    container_element: ".grid_container",
    next_token_element: ".next_token",
    failure_counter: 0,
    failure_counter_element: ".failure_counter",
    hint_element: ".hint",
    setup: function( gamestate )
    {
        game.gamestate = gamestate;
        $(game.grid_element).grid( { x:gamestate.width, y:gamestate.height,size: 50, drop_token:game.drop_token } ); 
        $(game.container_element).boxy( ); 
        $(game.hint_element).click(game.hint);
        game.update( gamestate );
        
        console.log( game); 
    },
    error_fn: function( message )
    {
        return function(){
            console.log( message );
            game.message( message );
        }
    },
    message: function( message )
    {
        alert( message );
    },
    update: function( result )
    {
        console.log( result );
        game.is_still_playable( result );
        if( result.success === false ) 
        {
            console.log( "Move failed." );
            // Update failure count
            game.set_failure_counter( result.failureCounter );
            // Reset token 
            game.next_token();
        } 
        else
        {
            console.log( "Move successful." );
            console.log( result );
            // Update board
            game.make_moves( result.update ); 
            // Update failure count
            game.set_failure_counter( result.failureCounter );
            // Set next token
            game.gamestate.currentToken = result.currentToken; 
            // Show next token 
            game.next_token();
        }
    },
    drop_token: function( token, x, y )
    {
        flup.attempt_move( { 
            mongo_id: game.mongo_id,
            point: x + "-" + y,
            last_move: game.last_move,
            success_callback: game.update,
            failure_callback: game.error_fn( "Can't find the server.") 
        });
        console.log( "Drop:", token, x, y )
    },
    hint: function( )
    {
        flup.hint( { 
            mongo_id: game.mongo_id,
            last_move: game.last_move,
            success_callback: game.update
        });
    },
    is_still_playable: function( result )
    {
        if( result.playable === undefined )
        {
            game.message( "An error has occurred! : \n" + result ); 
            return;
        }
        // Check if you win or lose
        if( result.playable != "Playable" )
        {
            game.message( "You " + result.playable );
            return false;
        }
        else
        {
            return true;
        }
    },
    make_moves: function( moves )
    {
        for( var i = 0; i < moves.length; i++ ) 
        {
            game.make_move( moves[i] )
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
        else if( move.namename === "doNothing" )
        {
            // do ... nothing. 
        } 
        game.last_move = move.sequence;
    },
    next_token: function( )
    {
        var token_element = $(game.next_token_element)
        token_element.html( token_lib.create_token( game.gamestate.currentToken ).draggable({
            revert:'invalid' 
        } )); 
    },
    set_failure_counter: function( new_counter ) 
    {
        new_counter = parseInt( new_counter, 10 );
        var diff = new_counter - game.failure_counter;
        game.failure_counter = new_counter;
        $(game.failure_counter_element).val( new_counter );
    }

}


$(document).ready(function() {
    game.mongo_id = window.location.href.split("#")[1];
    if( game.mongo_id === undefined ){
        window.location = "index.html";
    }
    
    flup.get_complete_state( { 
        mongo_id: game.mongo_id,
        success_callback: game.setup,
        failure_callback: game.error_fn("Couln't load page.")
    });
});

