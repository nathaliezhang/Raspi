#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

# custom HTTPrequestHandler class
class Server(BaseHTTPRequestHandler):
	
    #response to a get request
    def do_GET(self):
		root_dir = '/home/pi/server/web-server/'
		html_file = root_dir + 'index.html'
		
		try:
			if os.path.isfile(html_file):
				file = open(html_file)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(file.read())
				file.close()
		except: 
			print "Le fichier n'existe pas"

def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('192.168.43.70', 8080)
    http_connexion = server_class(server_address, handler_class)
    print "web server is running..."
    http_connexion.serve_forever() 

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
