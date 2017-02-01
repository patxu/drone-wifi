import SocketServer
import numpy as np
import matplotlib.pyplot as plt

curr_data = [30,30,30]
curr_names = ("Node 1", "Node 2", "Node 3")
labels =  np.arange(len(curr_names))

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data

        data_recieved = self.data.split('\n')

        for data_line in data_recieved:
            data = data_line.split(" ")

            try:
                name = int(data[0]) - 1;
                signal_strength = data[1]

                curr_data[name] = abs(int(signal_strength));

                plt.clf()

                colors = ['r', 'g', 'b']
                plt.bar(labels, curr_data, align='center', alpha=0.5, color = colors)
                plt.xticks(labels, curr_names)
                plt.ylabel('Signal Stength')
                plt.title('Triangulation')

                plt.draw()
                plt.pause(0.01)

            except Exception, e:
                raise e

        # just send back the same data, but upper-cased
        self.request.sendall("ACK")

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    plt.ion()

    colors = ['r', 'g', 'b']
    plt.bar(labels, curr_data, align='center', alpha=0.5, color = colors)
    plt.xticks(labels, curr_names)
    plt.ylabel('Signal Stength')
    plt.title('Triangulation')
     
    plt.draw()
    plt.pause(0.01)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()