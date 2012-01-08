
var setup = function( gamestate )
{
    console.log( gamestate )
    cube_grid(".cube_grid", gamestate.height, gamestate.width, 50 )      

}

$(document).ready(function() {
    mongo_id = window.location.href.split("#")[1];
    if( mongo_id === undefined ){
        window.location = "index.html";
    }
    
    flup.get_complete_state( { 
        mongo_id: mongo_id,
        success_callback: setup
    });
});

