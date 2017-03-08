import socket               # Import socket module
import thread
import threading
import numpy as np
import matplotlib.pyplot as plt
import time
import re
import sys

array_lock = threading.Lock()
# Start Graph
curr_data = [0, 0]
scale = [1, 0.7]
curr_names = ("Node 1", "Node 2")
labels = np.arange(len(curr_names))


def on_new_client(clientsocket, addr):
    # Signals Tracking
    signals, dblist = [[], []], [0, 0]
    d_thresh, dbupdate = 3, False
    signal_strength = 0

    while True:
        data = clientsocket.recv(1024)
        if not data:
            break

        data_recieved = data.split('\n')
        for data_line in data_recieved:
            data_col = data_line.split(" ")

            try:
                name = int(data_col[0]) - 1
                # extract signal(db) strength string from data
                db_string = re.search("(?<= -).*(?=dB)", data_line)
                # if found signal strength(dB) in data
                if db_string:
                    # append clients db strength value to its signal array sublist
                    signals[name].append(abs(int(db_string.group())))

                    # get new (average) signal strength, once enough data points gathered from a tracker
                    if len(signals[name]) >= 5:
                        dbupdate = True
                        new_signal_strength = scale[name]*sum(signals[name])/len(signals[name])
                        print "Client: {0}, RSSI: {1}".format(name, new_signal_strength)

                        # identify direction of movement of target
                        # same position
                        if dblist[name] - d_thresh < new_signal_strength < dblist[name] + d_thresh:
                            # print "Same as before from {0}".format(name)
                            pass
                        # move towards tracker
                        elif new_signal_strength < dblist[name]:
                            print "Closer to {0}".format(name+1)
                        else:  # move away from tracker
                            print "Further from {0}".format(name+1)
                        dblist[name] = new_signal_strength
                        signal_strength = new_signal_strength
                        signals[name] = []  # reset signals from tracker

                # array_lock.acquire()
                if dbupdate:
                    curr_data[name] = signal_strength
                    dbupdate = False
                # array_lock.release()

            except Exception, e:
                pass # print e

        # print "Client Says: "+data
        clientsocket.sendall("\n")
    clientsocket.close()


def plot_thread():
    plt.ion()

    colors = ['r', 'g']

    fig = plt.figure()
    bars = plt.bar(labels, [0,0], align='center', alpha=0.5, color=colors)
    plt.xticks(labels, curr_names)
    plt.ylabel('Signal Stength')
    plt.title('Triangulation')
    plt.ylim(20, 70)

    plt.draw()

    while True:
        plt.clf()

        colors = ['r', 'g']

        array_lock.acquire()
        plt.bar(labels, curr_data, align='center', alpha=0.5, color=colors)
        array_lock.release()

        plt.xticks(labels, curr_names)
        plt.ylabel('Signal Stength')
        plt.title('Triangulation')
        plt.ylim(20, 70)

        plt.draw()

        plt.pause(0.2)


if __name__ == '__main__':
    # Create TCP Socket
    s = socket.socket()         # Create a socket object
    host = "0.0.0.0"            # Get local machine name
    port = int(sys.argv[1])     # Reserve a port for your service.

    # Create Plotting Thread
    thread.start_new_thread(plot_thread, ())

    # Start Server
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    print 'Server started!\nWaiting for clients...'

    while True:
        c, addr = s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        thread.start_new_thread(on_new_client, (c, addr))

        # Note it's (addr,) not (addr) because second parameter is a tuple
        # Edit: (c,addr)
        # that's how you pass arguments to functions when creating new threads using thread module.
    s.close()
