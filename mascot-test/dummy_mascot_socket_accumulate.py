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
lineCount =0

trace_line = trace_file.read()
event_list =json.loads(trace_line)

trace_file.close()


trace_list = []

for event in event_list:
    # pop from the event_list and add to the trace_list
    trace_list.append(event_list.pop())

    # send current trace (trace_list) to Varanus
    line = json.dumps(trace_list)
    varanus_socket.send(line)
    print(line)

    #Check reply
    data = varanus_socket.recv(BUFFER_SIZE)
    print "received data: ", data

varanus_socket.close()
