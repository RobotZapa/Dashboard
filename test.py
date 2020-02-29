import dashboard

def visual_test():
    window = dashboard.WindowGrid(2, 2, "1920x1080", name='Test')
    gauge = dashboard.gauge.Gauge(window, 'Pressure', col=0, row=0, domain=(0, 101), inlay=20)
    graph = dashboard.graph.LiveGraph(window, 'Testing', col=1, row=0, domain=(-50, 50))
    gauge.test()
    graph.test()
    while True:
        window.update()
        window.delay(16)

if __name__ == "__main__":
    visual_test()
