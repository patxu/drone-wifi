import socket               # Import socket module
import thread
import numpy as np
import matplotlib.pyplot as plt

#Start Graph
curr_data = [0,0,0]
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

def on_new_client(clientsocket,addr):
    while True:
      data = clientsocket.recv(1024)

      if not data: break

      data_recieved = data.split('\n')

      for data_line in data_recieved:
          data_col = data_line.split(" ")

          try:
              name = int(data_col[0]) - 1;
              signal_strength = data_col[1][:-2]

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
              print "Invalid Input"

      print "Client Says: "+data
      clientsocket.sendall("\n")
    clientsocket.close()

s = socket.socket()         # Create a socket object
host = "localhost" # Get local machine name
port = 9998                # Reserve a port for your service.

print 'Server started!'
print 'Waiting for clients...'

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   thread.start_new_thread(on_new_client,(c,addr))
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
s.close()