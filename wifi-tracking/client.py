import fileinput
import socket
import sys
import subprocess as sub

if __name__ == "__main__":
    # connect client to server
    host = sys.argv[1]
    port = int(sys.argv[2])                   # The same port as used by the server
    name = int(sys.argv[3])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # print sys.argv

    mac = '9c:b6:d0:15:e3:eb'

    print "Hello :)"
    args = ['sudo', 'tcpdump', '-s', '0', '-tttt', '-vvvv', '-l', '-i', 'mon0', 'ether', 'src', mac]
    p = sub.Popen(args, stdout=sub.PIPE)

    for row in iter(p.stdout.readline, b''):
        s.sendall(str(name) + " " + row)
        print row

    # # read data stream from stdin and push to client over tcp4 socket
    # for line in fileinput.input():
    #     s.sendall("1 " + line)
    #     print line

    # close connection
    s.close()
    print('Received', repr(data))

