$(document).ready(function() {
    var currentRotation = 0;
    var tickOne = function()
    {
        currentRotation -= 3;
        $('.title_clock').css({
                'transform': 'rotate('+currentRotation+'deg)',
                '-moz-transform': 'rotate('+currentRotation+'deg)',
                '-o-transform': 'rotate('+currentRotation+'deg)',
                '-webkit-transform': 'rotate('+currentRotation+'deg)'
            }); 
    };
    var twoRotation = 0;
    var tickTwo = function()
    {
        twoRotation += 5;
        $('.title_hand').css({
                'transform': 'rotate('+twoRotation+'deg)',
                '-moz-transform': 'rotate('+twoRotation+'deg)',
                '-o-transform': 'rotate('+twoRotation+'deg)',
                '-webkit-transform': 'rotate('+twoRotation+'deg)'
            }); 
    };
    setInterval( tickOne, 2000 );
    setInterval( tickTwo, 4000 );
});
