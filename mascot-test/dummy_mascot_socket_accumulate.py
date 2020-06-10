import socket
import json

""" Reads the json file supplied in FILE, converts it to a list, and accumulates a trace.
    After each event, it sends the new Trace to Varanus """

TCP_IP = '127.0.0.1'
TCP_PORT = 5088
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
FILE = "scenario-traces/scenario1-trace.json"

#Open socket to Varanus
varanus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
varanus_socket.connect((TCP_IP, TCP_PORT))

trace_file = open(FILE, "r")

event_list =json.load(trace_file)

trace_file.close()

for event in event_list:

    # send current event to Varanus
    print("*** Dummy MASCOT Sent: " + event " ***")
    varanus_socket.send(event)

    #Check reply
    data = varanus_socket.recv(BUFFER_SIZE)
    print("*** Dummy MASCOT Received: " + data + " ***")

varanus_socket.close()
