import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
FILE = "dummy_mascot_data.json"

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
