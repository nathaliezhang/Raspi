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
                #os.system('lpr -o fit-to-page ' + filename + fileformat + '')
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
        #title = "Un chat blanc tacheté d'orange sous l'océan"
        #story = "Il y a bien longtemps, un chat. Il était blanc tacheté d’orange. Il n’avait qu’un seul œil et adorait jouer avec les poissons. Un jour, il plongea au coeur de la jungle. Malheureusement, il se rendit compte qu'il ne savait pas nager. Heureusement, il était assez fou pour quand même se jeter à l'eau.@Tout à coup, un poisson rouge vint à sa rencontre. Le chat intrigué, s’approcha de ce dernier. Il lui tendit la patte. Le poisson ne comprenant pas son geste eu peur et s’enfuit à toute vitesse.@Puis, il alla se cacher derrière un rocher. De temps en temps, il jetait des coups d'oeil dans la direction du chat. Surpris, ce dernier parti de nouveau à sa rencontre. C'est alors qu'un sorcier surgit de nulle part, il jeta un sort et éclata de rire. Il transforma le chat en poisson. Ne voyant pas le chat, le poisson sorti de sa cachette.@Ensuite, il vit un poisson chat sans se douter une seconde de sa véritable identité. Le poisson chat tout heureux s’approcha de lui.@Depuis ce jour, ils furent inséparables. C'est ainsi que débuta leur amitié. Désormais, ils étaient attachés l'un à l'autre."    
        
        title = "Une coccinelle qui voulait grandir au beau milieu d'un désert"
        story = "Il était une fois, une coccinelle qui voulait grandir. Elle ressemblait à un singe. La coccinelle avait pour habitude de nager dans les oasis aux alentours. Ses activités préférés étaient de plonger. Mais pour une fois, elle dansait toute la nuit au beau milieu d'un désert. @Soudain, un train apparut. Elle commença à plonger dans un chaudron. Après cette aventure, elle prit un bain. C'est alors qu'un sorcier surgit de nulle part, tendit une cuillère avant de diparaitre à nouveau. @Finalement, elle se servit de la cuillère pour se laver. @Depuis ce jour, elle est rayonnante et s’enflamma."
        paper.text_in_img(unicode(title, 'UTF8'), unicode(story, 'UTF8'))
        # os.system('lpr ' + filename + fileformat + '')
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
    
