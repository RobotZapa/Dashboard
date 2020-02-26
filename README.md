Dashboard lets you create a relatively simple GUIs quickly.
Using a grid system and Control/Display tiles that go into them.

**WindowGrid** (cols,rows,size,name)
    this creates a window that contains the grid for all your tiles.
    You tell it a number of columns wide by a number of rows tall.
    The size is any resolution as a string ea: "1440x720" and can include "fullscreen" if you need that.
    You can specify a icon with the icon keyword argument and a string to the file.
    The WindowGrid returns an object that must be passed to each tile you create.

*Here is a working example*::

    window = WindowGrid(16, 9, "1920x1080 fullscreen", name='Test')
    guage = GaugeTile(window, 'Pressure', row=(2, 3), col=(0, 1), domain=(0, 101), inlay=20)

**Gauge**
