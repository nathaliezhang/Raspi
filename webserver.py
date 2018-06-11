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
	print load_json
	
	if load_json["action"] == "shutdown":
            os.system('sudo shutdown -h now')
            
        elif load_json["action"] == "testConnection":
            print "Receive"
            
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
        
        title = "Un bonhomme nommé Sam le chasseur au coeur de la jungle"
        story = "Il était une fois, un petit bonhomme nommé Sam. Il portait toujours un chapeau sur la tête. Sam avait pour habitude de parcourir la savane tous les étés. Mais cette fois-ci, il décida de partir au coeur de la jungle.@Soudain, il rencontra un serpent lors d’un détour. Il n’avait pas peur de lui. En effet, il était habitué à rencontrer des animaux lors de ses voyages. Après cet évènement, Il décida d’aller rendre visite aux crocodiles. C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! La plante gênait le passage. @Malheureusement, il le transforma lui-même en un crocodile. @Et c'est ainsi qu’il décida de rester animal toute sa vie."
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
    
