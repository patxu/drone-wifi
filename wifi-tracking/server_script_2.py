import socket
import numpy as np
import matplotlib.pyplot as plt

#Start Graph
curr_data = [0, 0, 0]
curr_names = ("Node 1", "Node 2", "Node 3")
labels =  np.arange(len(curr_names))

plt.ion()

colors = ['r', 'g', 'b']
plt.bar(labels, curr_data, align='center', alpha=0.5, color = colors)
plt.xticks(labels, curr_names)
plt.ylabel('Signal Stength')
plt.title('Triangulation')
 
plt.draw()
plt.pause(0.01)
#########################


host = 'localhost'        # Symbolic name meaning all available interfaces
port = 9999     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print host , port
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:

    try:
        data = conn.recv(1024)

        if not data: break

        data_recieved = data.split('\n')

        for data_line in data_recieved:
            data_col = data_line.split(" ")

            try:
                name = int(data_col[0]) - 1;
                signal_strength = data_col[8][:-2]
                print "RSSI: ", signal_strength
                curr_data[name] = abs(int(signal_strength));

                plt.clf()

                colors = ['r', 'g', 'b']
                plt.bar(labels, curr_data, align='center', alpha=0.5, color = colors)
                plt.xticks(labels, curr_names)
                plt.ylabel('Signal Stength')
                plt.title('Triangulation')
                plt.ylim(20, 120)
                plt.draw()
                plt.pause(0.01)

            except Exception, e:
                pass # print "Invalid Input: " + ' '.join(data_col)

        #  print "Client Says: "+data
        conn.sendall("\n")

    except socket.error:
        print "Error Occured."
        break

conn.close()
