// element_selector is the selector for the element that will be filled with cube-grid.
// X is the number of horizontal squares in the cube grid. 
// Y is the number of vertical squares in the cube grid. 
// Size is the size of cubes in the grid. 
function cube_grid( element_selector, x, y, size )
{
    var cube_grid = "";

    var total_height = y * size;
    var total_width = x * size; 

    cube_grid += "<div style='position: absolute; top:0; width:"+total_width+"px; height:"+total_height+"px;' >";
    cube_grid += "<table>";

    var counter = 0;
    for( var i = 0; i < x; i++ ) 
    {
        cube_grid += "<tr>";
        for( var j = 0; j < y; j++)
        {
            var background_color = counter % 2 == 0 ? 'blue' : 'pink';
            cube_grid += "<td style='height:"+size+"px; width:"+size+"px; background-color:"+background_color+";' ></td>";
            counter ++;
        }
        cube_grid += "</tr>";
        counter ++;
    }
    cube_grid += "</table>";
    
    $(element_selector).css('overflow', 'hidden');
    $(element_selector).css('position', 'relative');
    $(element_selector).append( cube_grid );
}
