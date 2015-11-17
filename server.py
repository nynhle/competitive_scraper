import SimpleHTTPServer
import SocketServer

def run_server():
	PORT = 8000

	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), handler)

	print "Server is running on port " + str(PORT)
	httpd.serve_forever
