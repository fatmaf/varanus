#!/usr/bin/env python
import argparse
import time

import dummy_mascot_socket_test


argParser = argparse.ArgumentParser()
argParser.add_argument("file", help="The file to read from.")

args = argParser.parse_args()
FILE = args.file

IP = '127.0.0.1'
PORT = 5088
BUFFER_SIZE = 1024


mascot_socket, varanus_socket = dummy_mascot_socket_test.start(IP, PORT)

dummy_mascot_socket_test.read_and_send(varanus_socket, FILE, BUFFER_SIZE)

dummy_mascot_socket_test.end(mascot_socket, varanus_socket)
