import socket

host = 'localhost'   # Symbolic name meaning all available interfaces
port = 9999          # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create IPv4 socket
s.bind((host, port))  # bind socket to host:port

print host , port
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    try:
        data = conn.recv(1024)
        if not data: break
        print "rssi:", data.split()[7][:-2]
        conn.sendall("Server Says:hi")

    except socket.error:
        print "Error Occured."
        break

conn.close()
