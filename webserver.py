#!/usr/bin/env python
# coding: utf8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import commands
from PIL import Image, ImageDraw, ImageFont
import textwrap

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
	except : 
	    print "Le fichier n'existe pas"
	
    #response to a post request	
    def do_POST(self):
	length = int(self.headers['Content-Length'])
	data = self.rfile.read(length)
	split_data = data.split('=')
	story = split_data[1] #retrieve the text
	# TODOreturn header and change status
	
	# run the command to print the image
	filename = "texts/story"
	fileformat = ".png"
	width = 384
	bg_color = "#FFF"
	#font = 'fonts/Maison-Neue/Maison Neue Book.otf'
	font = 'fonts/Editor/Editor-Medium.ttf'
	font_size = 25
	text_transform(story, filename, fileformat, width, bg_color, font_size)
	#os.system('lpr -o fit-to-page ' + filename + fileformat + '')
	#os.system('lpr ' + filename + fileformat + '')
	print story
		
def run(server_class=HTTPServer, handler_class=Server):
	host = commands.getoutput('hostname -I') #raspberry IP : depending the network
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	text_transform("Il était une fois, des tortues géantes qui nageaient dans l'océan Atlantique.", "texts/story", ".png", 384, "#FFF", 25, text_color='#000')
	http_connexion.serve_forever()
	
# transform the text in png
def text_transform(text, filename, fileformat, width, bg_color, font_size, text_color='#000'):
    # TODO change the hight according the lines number -> see multiline_textsize
    height = 500
    img = Image.new('L', (width, height), bg_color)
    medium_font = 'fonts/Editor/Editor-Medium.ttf'
    bold_font = 'fonts/Editor/Editor-Bold.ttf'
    text_medium_font = ImageFont.truetype(medium_font, font_size, encoding="unic")
    text_bold_font = ImageFont.truetype(bold_font, font_size, encoding="unic")
    context = ImageDraw.Draw(img) #create a drawing context
    
    custom_words = [
        "Il était une fois",
        "C'est l'histoire des",
        "Il y a bien longtemps",
        "qui",
        "et",
        "Soudain",
        "Un jour",
        "Tout à coup"
    ]
    
    #textwrap 
    story_lines = textwrap.wrap(text, width=30)
    left = 10
    top = 30
    for story_line in story_lines:
        
        font_width, font_height = text_medium_font.getsize(text)
        
        # TODO prepare the text treatment : images, fonts... : go trought the text to detect words
        for expression in custom_words:
            #print story_line
            begin_expression = story_line.find(expression)
            #print begin_expression
            if begin_expression >= 0: #has the expression
                end_exppresion = begin_expression + len(expression)
            else:
                end_exppresion = begin_expression  
            #print end_exppresion
        
        story_line = unicode(story_line, 'UTF-8') #correct the characters for printing
        context.multiline_text((left,top), story_line, fill=text_color, font=text_medium_font) #draw text
        
        top += font_height
    del context #destroy drawing context
    img.save(filename + fileformat, "PNG")
    

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
