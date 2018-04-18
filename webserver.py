#!/usr/bin/env python
# coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import commands
from PIL import Image, ImageDraw, ImageFont

# custom HTTPrequestHandler class
class Server(BaseHTTPRequestHandler):
	
    #response to a get request
    def do_GET(self):
        #root_dir = '/home/pi/server/web-server/'
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
	except: 
	    print "Le fichier n'existe pas"
	
    #response to a post request	
    def do_POST(self):
	length = int(self.headers['Content-Length'])
	data = self.rfile.read(length)
	split_data = data.split('=')
	story = split_data[1] #retrieve the text
	# TODOreturn header and change status
	
	# run the command to print the image
	filename = "texts/text-1"
	fileformat = ".png"
	text_transform(story, filename, fileformat)
	os.system('lpr -o fit-to-page ' + filename + fileformat + '')
	print story
		
def run(server_class=HTTPServer, handler_class=Server):
	host = commands.getoutput('hostname -I') #raspberry IP
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	http_connexion.serve_forever()
	
# transform the text in png
def text_transform(text, filename, fileformat, width=384, bg_color='#FFF', font='fonts/Maison-Neue/Maison Neue Book.otf', font_size=10, text_color='#000'):
    # TODO change the hight according the lines number -> see multiline_textsize
    # TODO prepare the text treatment : images, fonts...
    height = 200
    img = Image.new('L', (width, height), bg_color)
    text_font = ImageFont.truetype(font, font_size)
    context = ImageDraw.Draw(img) #create a drawing context
    context.text((10,10), text, font=text_font, fill=text_color) #draw text
    del context #destroy drawing context
    img.save(filename + fileformat, "PNG")
    

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
