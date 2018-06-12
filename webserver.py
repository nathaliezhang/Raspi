#!/usr/bin/env python
# coding: utf8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import commands
import json
import storydesign
from PIL import Image

# custom HTTPrequestHandler class
class Server(BaseHTTPRequestHandler):
	
    #response to a get request
    def do_GET(self):
        root_dir = '/home/pi/Raspi/'
        html_file = root_dir + 'index.html'
		
	try:
            if os.path.isfile(html_file):
		file = open(html_file)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(file.read())
		file.close()          
	except : 
	    print "Le fichier n'existe pas"
	
    #response to a post request	
    def do_POST(self):
	length = int(self.headers['Content-Length'])
	data = self.rfile.read(length) #retrieve a json string from the app
	load_json = json.loads(data) # convert
	print load_json
	
	if load_json["action"] == "shutdown":
            os.system('sudo shutdown -h now')
            
        elif load_json["action"] == "testConnection":
            print "Receive"
        
        elif load_json["action"] == "greeting":
            os.system('lpr -o fit-to-page assets/img/bonjour.jpg')
            
        elif load_json["action"] == "print":
            story = load_json["text"]
            title = load_json["title"]
            quantity = load_json["quantity"]
            
            # run the command to print the image
            paper = storydesign.StoryDesign()
            filename = paper.filename
            fileformat = paper.fileformat
            paper.text_in_img(title, story)
            print title
            print story
            
            # print the quantity choose
            copy = 0
            while copy < quantity:
                os.system('lpr -o fit-to-page ' + filename + fileformat + '')
                #os.system('lpr ' + filename + fileformat + '')
                copy += 1
	
	self.send_response(200) # return status
	self.send_header('Content-type','text/html') # return header
	self.end_headers()
		
def run(server_class=HTTPServer, handler_class=Server):
    
        #local story design
        paper = storydesign.StoryDesign()
        filename = paper.filename
        fileformat = paper.fileformat
        
        title = "Thierry le professeur de BDDI qui voulait que toute la classe réussisse son jury sur la lune"
        story = "Il était une fois, Thierry le professeur de BDDI qui voulait que toute la classe réussisse son jury. Il aimait la pluie. Thierry  avait pour habitude de faire le mini golf avec des singes. Mais cette fois-ci, il se prélassait dans les remous sur la lune. @Tout à coup, un dragon surgit. Thierry essaye de se réfugier dans une grotte. Peu de temps après, il s’endormit. C'est alors qu'une guerrière apparut et lança un défi : réussir à la battre à l'épée. @Malheureusement, Thierry n’avait pas envie de se battre. Il lui proposa plutôt d’aller s’en prendre au dragon. @Et c'est ainsi que Thierry put se débarrasser des troubles fêtes de son repos"
        paper.text_in_img(unicode(title, 'UTF8'), unicode(story, 'UTF8'))
        # os.system('lpr ' + filename + fileformat + '')
        
	host = commands.getoutput('hostname -I') #raspberry IP : depending the network
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	http_connexion.serve_forever()
        

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
    
