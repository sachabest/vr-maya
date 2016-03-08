#!/usr/bin/python
# TCP Frame Tester

HOST, PORT = "localhost", 10000
MAX_IMAGE_SIZE = 1024 * 1024 * 4 # 8MB
OK_SIZE = 1024
IMG_BUF = 8

import sys, socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to server and send data
    print "Listening on %s:%d" % (HOST, PORT)
    sock.bind((HOST, PORT))
    sock.listen(10)
    conn, addr = sock.accept()
    print "Receiving from %s:%d" % addr
    while True:
        ## get size 
        data = conn.recv(OK_SIZE).strip()
        length = int(data)
        print "Receiving " + str(length) +  " bytes"
        conn.send("k\n")
        print "Acknowledged"

        ## get frame
        data = conn.recv(length + IMG_BUF).strip()
        print "Received " + str(len(data)) +  " bytes"
        conn.send("k\n")
        print "Acknowledged"

finally:
    conn.close()
    sock.close()