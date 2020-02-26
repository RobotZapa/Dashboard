import dashboard.window
import dashboard.gauge
import dashboard.graph

def visual_test():
    window = dashboard.WindowGrid(2, 2, "1920x1080", name='Test')
    guage = dashboard.gauge.GaugeTile(window, 'Pressure', col=0, row=0, domain=(0, 101), inlay=20)
    graph = dashboard.graph.GraphTile(window, 'Testing', col=1, row=0, domain=(-50, 50))
    guage.test()
    graph.test()

if __name__ == "__main__":
    visual_test()