# TCP Frame Tester

HOST, PORT = "localhost", 10000
MAX_IMAGE_SIZE = 1024 * 1024 * 2 # 2MB

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall("k")

if __name__ == "__main__":
    print 'Starting listen socket on ' + HOST + ":" + str(PORT)
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()