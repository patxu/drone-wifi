import fileinput
import socket

if __name__ == "__main__":
    # connect client to server
    host = "localhost"
    port = 9999                   # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # read data stream from stdin and push to client over tcp4 socket
    for line in fileinput.input():
        s.sendall(line)

    # close connection
    s.close()
    print('Received', repr(data))
