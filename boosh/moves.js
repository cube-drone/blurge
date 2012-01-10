
var move_lib = {
    move_to_object:function( move ) 
    {
        return { 
            sequence: move[0],
            movename: move[1],
            token: move[2],
            x: move[3][0],
            y: move[3][1]
        }; 
    }
}
