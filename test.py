import dashboard

def visual_test():
    cols = 10
    rows = 10
    window = dashboard.WindowGrid(cols, rows, "1920x1080", name='Test')
    mod = 4
    for col in range(cols):
        for row in range(rows):
            #gauge = dashboard.gauge.Gauge(window, 'Pressure', col=col, row=row, domain=(0, 101), inlay=20)
            graph = dashboard.graph.LiveGraph(window, 'Testing', col=col, row=row, domain=(-50, 50), zoom=1+(row+col)%mod)
            #gauge.test()
            graph.test()
    while True:
        window.update()
        window.sleep(16)

if __name__ == "__main__":
    visual_test()
