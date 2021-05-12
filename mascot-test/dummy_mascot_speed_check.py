import argparse
import time

import dummy_mascot_socket_test


argParser = argparse.ArgumentParser()
argParser.add_argument("file", help="The file to read from.")


IP = '127.0.0.1'
PORT = 5088
BUFFER_SIZE = 1024


mascot_socket, varanus_socket = dummy_mascot_socket_test.start(IP, PORT)

for i in range(10):
    read_and_send(varanus_socket, FILE, BUFFER_SIZE)
    time.sleep(1)

end(mascot_socket, varanus_socket)
