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

    macs = {'vp': '4c:66:41:3f:61:7a', 'ap': 'ec:1f:72:34:97:2b', 'dp': 'f4:f5:23:3c:8e:08'}
    mac = macs[sys.argv[4]]

    print "Hello :)"
    args = ['sudo', 'tcpdump', '-s', '0', '-tttt', '-vvvv', '-l', '-i', 'mon0', 'ether', 'src', mac]
    p = sub.Popen(args, stdout=sub.PIPE)

    for row in iter(p.stdout.readline, b''):
        s.sendall(str(name) + " " + row)
        print row

    # close connection
    s.close()
