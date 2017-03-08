import matplotlib.pyplot as plt

NODE_SIZE = .2

def drawNode(node, ax):
    center = plt.Circle((node.x, node.y), NODE_SIZE, color=node.main_color)
    signal = plt.Circle((node.x, node.y), node.signal, color=node.signal_color, fill=False, clip_on=False)
    ax.add_artist(center)
    ax.add_artist(signal)

class Node(object):
    def __init__(self, x, y, main_color, signal, signal_color):
        self.x = x
        self.y = y
        self.main_color = main_color
        self.signal = signal
        self.signal_color = signal_color

    def __str__(self):
        return "Node(%s,%s), Signal Strength:%s"%(self.x, self.y, self.signal)

def configPlot(ax):
    plt.figure(1)
    plt.title("Wifi Triangulation Vizualization")
    plt.axis('equal')
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 10))

if __name__ == '__main__':
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
    configPlot(ax)

    nodes = [Node(2, 2, '#F44336', 2, '#EF9A9A'),
             Node(2, 4, '#4CAF50', 2, '#A5D6A7'),
             Node(6, 2, '#2196F3', 2, '#90CAF9')]

    for node in nodes:
        drawNode(node, ax)

    fig.savefig('plot.png')
