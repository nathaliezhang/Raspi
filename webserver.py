#!/usr/bin/env python
# coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import commands
import Image

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
	
    #response to a post request	
    def do_POST(self):
	length = int(self.headers['Content-Length'])
	data = self.rfile.read(length)
	split_data = data.split('=')
	text = split_data[1]
	print text
	#return header and change status
	#transform the text in png
	#prepare the text treatment : images, fonts...
	#run the command to print the image
		
def run(server_class=HTTPServer, handler_class=Server):
	host = commands.getoutput('hostname -I') #raspberry IP
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	http_connexion.serve_forever() 

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
