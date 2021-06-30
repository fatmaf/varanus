import socket
import json

""" Reads the json file supplied in FILE, converts it to a list, and sends
    each event (one-by-one) to Varanus """



def start(tcp_tp, tcp_port):
    #Open socket to Varanus
    mascot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mascot_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #varanus_socket.connect((TCP_IP, TCP_PORT))
    mascot_socket.bind((tcp_tp, tcp_port))
    mascot_socket.listen(1)

    print("*** Dummy Mascot Listening ***")
    varanus_socket, addr = mascot_socket.accept()
    return mascot_socket, varanus_socket


def read_and_send(varanus_socket, file_path, buffer_size ):
    print("*** Dummy Mascot Reading File ***")
    trace_file = open(file_path, "r")

    event_list =json.load(trace_file)

    trace_file.close()
    print("*** Dummy Mascot Sending ***")
    for event in event_list:

        # send current event to Varanus
        print("*** Dummy MASCOT Sent: " + event + " ***")
        varanus_socket.send(event)

        #Check reply
        data = varanus_socket.recv(buffer_size)
        print("*** Dummy MASCOT Received: " + data + " ***")

def end(mascot_socket, varanus_socket):
    mascot_socket.close()
    varanus_socket.close()

if __name__ == "__main__":

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5088
    BUFFER_SIZE = 1024
    FILE = "scenario-traces/scenario1-trace.json"

    mascot_socket, varanus_socket = start(TCP_IP, TCP_PORT)
    read_and_send(varanus_socket, FILE, BUFFER_SIZE)
    end(mascot_socket, varanus_socket)
