Dashboard lets you create a relatively simple GUIs quickly.
Using a grid system and Control/Display tiles that go into them.

# WindowGrid (cols,rows,size,name)
this creates a window that contains the grid for all your tiles.
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
    
## Gauge (window, name, col, row, domain)

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
