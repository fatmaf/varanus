import socket

""" Reads the json file supplied in FILE and sends this to the monitor """

TCP_IP = '127.0.0.1'
TCP_PORT = 5045
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
FILE = "mascot-speed-fail-am.json"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

f = open(FILE, "r")

for line in f:
    s.send(line)
    print "sent data: ", line
    data = s.recv(BUFFER_SIZE)
    print "received data: ", data

f.close()
s.close()
