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
            #os.system('lpr -o fit-to-page ' + filename + fileformat + '')
            os.system('lpr ' + filename + fileformat + '')
            copy += 1
	
	self.send_response(200) # return status
	self.send_header('Content-type','text/html') # return header
	self.end_headers()
		
def run(server_class=HTTPServer, handler_class=Server):
    
        #local story design
        paper = storydesign.StoryDesign()
        filename = paper.filename
        fileformat = paper.fileformat
        title = "Un chat sous l'océan"
        story = "C'est l'histoire d’un chat. Il était blanc tacheté d’orange. Il n’avait qu’un seul œil et adorait jouer avec les poissons. Un jour, il plongea sous l'ocean.@Soudain, un poisson rouge vint à sa rencontre. Le chat intrigué, s’approcha de ce dernier. Il lui tendit la patte. Le poisson ne comprenant pas son geste eu peur et s’enfuit à toute vitesse.@Puis, il alla se cacher derrière un rocher. Surpris, le chat parti de nouveau à sa rencontre. C'est alors qu'un sorcier surgit de nulle part, il jeta un sort et éclata de rire. Il transforma le chat en poisson. Ne voyant pas le chat, le poisson sorti de sa cachette.@Ensuite, Il vit un poisson chat sans se douter un seconde de sa véritable identité. Le poisson chat tout heureux s’approcha de lui.@Depuis ce jour, ils furent inséparables. FIN."    
        paper.text_in_img(unicode(title, 'UTF8'), unicode(story, 'UTF8'))
        #print story
        
	host = commands.getoutput('hostname -I') #raspberry IP : depending the network
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	http_connexion.serve_forever()
        

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
    
