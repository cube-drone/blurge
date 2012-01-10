
var token_lib = { 
    create_token:function( token_name ){
        return $("<div class='token "+token_name+"' ></div>").data("token_name",token_name);
    }
};
