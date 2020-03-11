import dashboard

def n_test():
    cols = 1
    rows = 1
    window = dashboard.WindowGrid(cols, rows, "1920x1080", name='Test')
    mod = 4
    for col in range(cols):
        for row in range(rows):
            gauge = dashboard.gauge.ArcGauge(window, 'Pressure', col=col, row=row, domain=(0, 101), inlay=20)
            #graph = dashboard.graph.LiveGraph(window, 'Testing', col=col, row=row, domain=(-50, 50), zoom=1+(row+col)%mod)
            gauge.test()
            #graph.test()
    while True:
        window.update()
        window.sleep(16)

def complex_test():
    cols = 3
    rows = 3
    window = dashboard.WindowGrid(cols, rows, "1920x1080", name='Test')
    tile = dashboard.TileGrid(window, 0, 0, 5, 4)
    lamp = dashboard.Indicator(tile, col=0, row=0, name="Chattering", on="warning.png", off=(50, 50, 50), text_on=(255, 255, 255), text_off=(20, 20, 20))
    lamp.test()
    gauge = dashboard.gauge.Gauge(window, 'Pressure', col=1, row=0, domain=(0, 101), inlay=20)
    graph = dashboard.graph.LiveGraph(window, 'RPM', col=2, row=0, domain=(-50, 50), zoom=1)
    gauge.test()
    graph.test()
    while True:
        window.update()
        window.sleep(16)


if __name__ == "__main__":
    complex_test()
