
var token_lib = { 
    create_token:function( token_name, token_class ){
        return $("<div class='token "+token_name+" "+token_class+"' ></div>").data("token_name",token_name);
    }
};
