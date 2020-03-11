Dashboard lets you create a relatively simple GUIs quickly.
Using a grid system and Control/Display tiles that go into them.

# WindowGrid (cols,rows,size,name)
This creates a window that contains the grid for all your tiles.
You tell it a number of columns wide by a number of rows tall.
The size is any resolution as a string ea: "1440x720" and can include "fullscreen" if you need that.
You can specify a icon with the icon keyword argument and a string to the file.
The WindowGrid returns an object that must be passed to each tile you create.

*Here is a working example*

    import dashboard as dash
    window = dash.WindowGrid(16, 9, "1920x1080 fullscreen", name='Test')
    gauge = dash.Gauge(window, 'Pressure', row=(2, 3), col=(0, 1), domain=(0, 101), inlay=20)
    while True:
        window.update() # on linux this is unessisary (check window.loop(framerate))
        window.sleep(16) # time in ms (or other sleep function)
        
# TileGrid (window, col, row, num_cols, num_rows)
This creates a tile that can be used in place of a WindowGrid.
It can be used as a sub-tiler for smaller elements like indicators and
buttons. 

*Here is a working example*

    import dashboard as dash
    window = dash.WindowGrid(16, 9, "1920x1080 fullscreen", name='Test')
    subtile = dash.TileGrid(window, 0, 0, 2, 2)
    lamp = dash.Indicator(subtile, col=0, row=0, name='Overflow, off=(50,50,50), on=(255,0,0)
    lamp.test()
    while True:
        window.update() # on linux this is unessisary (check window.loop(framerate))
        window.sleep(16) # time in ms (or other sleep function)
    
## Gauge (window, name, col, row, domain)
A simple gauge tile.

Arguments
1. window - the WindowGrid object
2. name - the functional name of the tile
3. col - an int or tuple of (start,stop) where it is located horizontally
4. row - an int or tuple of (start,stop) where it is located vertically
5. domain - and tuple of ints (start,stop) for the gauge to have as limits

Keywords arguments
* inlay = an int for the depth that the gauge is sunk into the frame in pixels
* unit_ticks = a boolean, true is all single digits in the domain should be marked
* tick_divisor = default is 10, an int for how many x ticks gives a big tick
* img_file = an image to use instead of automatically generating a gauge

## LiveGraph (window, name, col, row, domain)
A simple graphing tile, graphs a single value with respect to time.

Arguments
1. window - the WindowGrid object
2. name - the name of the graph
3. col - an int or tuple of (start,stop) where it is located horizontally
4. row - an int or tuple of (start,stop) where it is located vertically
5. domain - and tuple of ints (start,stop) for the gauge to have as limits

Keyword arguments
* zoom=1 - will make the time window shorter and the graph faster