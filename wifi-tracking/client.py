import fileinput
import socket
import sys

if __name__ == "__main__":
    # connect client to server
    host = "192.168.43.154"
    port = 9999                   # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # print sys.argv

    # read data stream from stdin and push to client over tcp4 socket
    for line in fileinput.input():
        s.sendall("2 " + line)

    # close connection
    s.close()
    print('Received', repr(data))
