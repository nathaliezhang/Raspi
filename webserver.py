#!/usr/bin/env python
# coding: utf8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import commands
import json
import storydesign

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
	story = load_json["text"]
	
	# run the command to print the image
	paper = storydesign.StoryDesign()
	filename = paper.filename
	fileformat = paper.fileformat
        paper.text_in_img(story)
	#os.system('lpr -o fit-to-page ' + filename + fileformat + '')
	os.system('lpr ' + filename + fileformat + '')
	print story
	
	self.send_response(200) # return status
	self.send_header('Content-type','text/html') # return header
	self.end_headers()
		
def run(server_class=HTTPServer, handler_class=Server):
    
        #local story design
        paper = storydesign.StoryDesign()
        filename = paper.filename
        fileformat = paper.fileformat
        story = "Il y a bien longtemps, un petit pois bien dodu au nom de Popo. Il adorait manger de la crème. Ses mains étaient vertes et sa frimousse aussi. Il chantait dans la jungle.@Tout à coup, un bruit s'abattu. Popo eu peur. Il décida de s'en aller plus loin. Ses jambes le portèrent jusqu'à une souche d'arbre.@Quelques heures plus tard, il s'assoupi de fatigue. Il fit de nombreux cauchemars."
        paper.text_in_img(unicode(story, 'UTF8'))
        print story
        
	host = commands.getoutput('hostname -I') #raspberry IP : depending the network
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	http_connexion.serve_forever()
        

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
    
