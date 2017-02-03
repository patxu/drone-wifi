import socket               # Import socket module
import thread
import threading
import numpy as np
import matplotlib.pyplot as plt
import time

array_lock = threading.Lock();

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
              signal_strength = data_col[8][:-2]
              print "RSSI: ", signal_strength

              array_lock.acquire()

              curr_data[name] = abs(int(signal_strength));

              array_lock.release()

          except Exception, e:
              print "Invalid Input"

      print "Client Says: "+data
      clientsocket.sendall("\n")
    clientsocket.close()

def plot_thread():
  while True:
    plt.clf()

    colors = ['r', 'g', 'b']

    array_lock.acquire()

    plt.bar(labels, curr_data, align='center', alpha=0.5, color = colors)

    array_lock.release()

    plt.xticks(labels, curr_names)
    plt.ylabel('Signal Stength')
    plt.title('Triangulation')
    plt.ylim(20, 120)
    plt.draw()
    plt.pause(0.01)

    time.sleep(0.3)

s = socket.socket()         # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 9998                # Reserve a port for your service.

print 'Server started!'
print 'Waiting for clients...'

thread.start_new_thread(plot_thread, ())

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