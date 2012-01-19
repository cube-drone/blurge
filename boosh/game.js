
var game = {
    mongo_id: "",
    gamestate: "",
    last_move: -1,
    grid_element: ".cube_grid", 
    container_element: ".grid_container",
    next_token_element: ".next_token",
    failure_counter: 0,
    failure_counter_element: ".failure_counter",
    hint_counter: 0,
    hint_element: ".hint",
    new_game_element: ".new_game", 
    is_loading: false,
    token_obfuscators: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
"L", "M", "N", "O", "P", "Q", "R"], 
    token_class_mappings: {},
    scrambled: true, 
    setup: function( gamestate )
    {
        game.loading( false );
        game.gamestate = gamestate;
        $(game.grid_element).grid( { x:gamestate.width, y:gamestate.height, size:52, drop_token:game.drop_token } ); 
        $(game.container_element).boxy( ); 
        $(game.hint_element).click(game.hint);
        $(game.new_game_element).click(game.new_game);

        if( 'tokens' in gamestate )
        {
            game.scrambled = false;
            for( var i = 0; i < gamestate.tokens.length; i++ )
            {
                game.token_class_mappings[ game.token_obfuscators[i] ] = gamestate.tokens[i];
            }
        }  
        
        game.update( gamestate );
        
        console.log( game); 
    },
    new_game: function( )
    {
        window.location = "index.html";  
    },
    error_fn: function( message )
    {
        return function(){
            console.log( message );
            game.message( message );
            game.loading( false );
        }
    },
    message: function( message )
    {
        alert( message );
    },
    update: function( result )
    {
        game.loading( false );
        console.log( result );
        game.is_still_playable( result );
        if( result.success === false ) 
        {
            game.hint_counter += 1;
            if( game.hint_counter == 3 )
            {
                $(".hint").effect("shake", {times:3}, 50);
                game.hint_counter = 0;
            }
            console.log( "Move failed. " + game.hint_counter );
             
            $(game.grid_element + " table").effect("shake", { times:3 }, 150);
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
    drop_token: function( x, y )
    {
        game.loading( true );
        flup.attempt_move( { 
            mongo_id: game.mongo_id,
            point: x + "-" + y,
            last_move: game.last_move,
            success_callback: game.update,
            failure_callback: game.error_fn( "Can't find the server.") 
        });
        console.log( "Attempt:", x, y )
    },
    hint: function( )
    {
        if( game.is_loading)
        {
            return; 
        }
        game.loading( true );
        flup.hint( { 
            mongo_id: game.mongo_id,
            last_move: game.last_move,
            success_callback: game.update, 
            failure_callback: game.error_fn( "Can't find the server. Hint failed.") 
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
            $(game.grid_element).grid( 'place', move.x, move.y, game.create_token( move.token ) );  
            // render this space unusable
            $(game.grid_element).grid( 'get', move.x, move.y).droppable('option', 'disabled', true );
            $(game.grid_element).grid( 'get', move.x, move.y).effect('highlight', { }, 2000);
        }
        else if( move.movename === "clearToken")
        {
            $(game.grid_element).grid( 'clear', move.x, move.y );  
            // this space becomes usable again. 
            $(game.grid_element).grid( 'get', move.x, move.y).droppable('option', 'disabled', false )
            $(game.grid_element).grid( 'get', move.x, move.y).effect('highlight', { }, 2000);
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
        token_element.html( game.create_token( game.gamestate.currentToken ).draggable({
            revert:'invalid' 
        } )); 
    },
    set_failure_counter: function( new_counter ) 
    {
        new_counter = parseInt( new_counter, 10 );
        var diff = new_counter - game.failure_counter;
        game.failure_counter = new_counter;
        $(game.failure_counter_element).val( new_counter );
        $(game.failure_counter_element).effect('highlight', {}, 2000);
    },
    loading: function( is_loading )
    {
        if(game.is_loading === is_loading)
        {
            return;
        }
        if(is_loading) 
        {
            game.is_loading = true;
            document.body.style.cursor = "wait"; 
        }
        if(! is_loading )
        {
            game.is_loading = false;
            document.body.style.cursor = "default";
        }
    },
    create_token:function( token_name ){
        var token_class = token_name;
        if (! game.scrambled)
        {
            token_class = game.token_class_mappings[token_name];
        }
        return $("<div class='token "+token_class+"' ></div>").data("token_name",token_name);
    }

}


$(document).ready(function() {
    game.mongo_id = window.location.href.split("#")[1];
    if( game.mongo_id === undefined ){
        window.location = "index.html";
    }
    game.loading( true );
    
    flup.get_complete_state( { 
        mongo_id: game.mongo_id,
        success_callback: game.setup,
        failure_callback: game.error_fn("Couldn't load page.")
    });
});

