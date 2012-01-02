""" Functions for dealing with moves. 

Moves are expected to be a tuple collection of 
    ( sequence, name of move, token, point ) 

"""
import tokens

def serialize_move( move ):
    movecounter, movename, token, point = move
    return ( movecounter, movename, token.serialize(), point )

def unserialize_move( move ):
    movecounter, movename, token, point = move
    return ( movecounter, movename, tokens.deserialize( token ), point ) 
