import socket

""" Reads the json file supplied in FILE and sends this to the monitor """

TCP_IP = '127.0.0.1'
TCP_PORT = 5044
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
FILE = "scenarios/scenario1.json"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

f = open(FILE, "r")
lineCount =0

for line in f:
    if line not in ['\n', '\r\n']:
        s.send(line)
        lineCount = lineCount +1
        print "Line Num: ", lineCount ,"sent data: ", line

        data = s.recv(BUFFER_SIZE)
        print "received data: ", data

f.close()
s.close()
