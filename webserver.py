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
	font = 'fonts/Editor/Editor-Medium.ttf'
	font_size = 25
	text_transform(story, filename, fileformat, width, bg_color, font_size)
	#os.system('lpr -o fit-to-page ' + filename + fileformat + '')
	#os.system('lpr ' + filename + fileformat + '')
	print story
	self.send_response(200)
	self.send_header('Content-type','text/html')
	self.end_headers()
		
def run(server_class=HTTPServer, handler_class=Server):
	host = commands.getoutput('hostname -I') #raspberry IP : depending the network
	port = 8080
	server_address = (host, port)
	http_connexion = server_class(server_address, handler_class)
	print "Web server is running on " + host + "..."
	#text_transform("Il était une fois, des tortues géantes qui nageaient dans l'océan Atlantique.", "texts/story", ".png", 384, "#FFF", 25, text_color='#000')
	http_connexion.serve_forever()
	
# transform the text in png
def text_transform(text, filename, fileformat, width, bg_color, font_size, text_color='#000'):
    # TODO change the hight according the lines number -> see multiline_textsize
    height = 500
    img = Image.new('L', (width, height), bg_color)
    book_font = 'fonts/Maison-Neue/Maison Neue Book.otf'
    bold_font = 'fonts/Maison-Neue/Maison Neue Bold.otf'
    text_book_font = ImageFont.truetype(book_font, font_size, encoding="unic")
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
    
    # text wrap
    story_lines = textwrap.wrap(text, width=25)
    top = 30
    
    for story_line in story_lines:
        show_sentence = 1
        font_width, font_height = text_book_font.getsize(text)
        
        # TODO prepare the text treatment : images, fonts... : go trought the text to detect words
        for expression in custom_words:
            
            begin = story_line.find(expression)
            left = 10
            
            if begin >= 0: #has the expression
                show_sentence = 0
                end = begin + len(expression)
                
                if begin == 0:
                    before = ""
                else:
                    before = story_line[0:begin]
                before_width, before_height = text_book_font.getsize(before)
                #print before_width
                before = unicode(before, 'UTF-8')
                context.multiline_text((left,top), before, fill=text_color, font=text_book_font)
                left = left + before_width

                strong = story_line[begin:end]
                strong_width, strong_height = text_bold_font.getsize(strong)
                #print strong_width, strong_height
                strong = unicode(strong, 'UTF-8')
                context.multiline_text((left,top), strong, fill=text_color, font=text_bold_font)
                left = left + strong_width
                
                if end == len(story_line):
                    after = ""
                else:
                    after = story_line[end:len(story_line)]
                after_width, after_height = text_book_font.getsize(after)
                #print after_width, after_height
                after = unicode(after, 'UTF-8')
                context.multiline_text((left,top), after, fill=text_color, font=text_book_font)
                #print before
                #print strong
                #print after
                break  
            else:
                end = begin
                
        if show_sentence == 1: #hasn't the expression
            #print story_line
            story_line = unicode(story_line, 'UTF-8')
            context.text((left,top), story_line, fill=text_color, font=text_book_font) # draw text
            
        #story_line = unicode(story_line, 'UTF-8') #correct the characters before printing
        #context.text((left,top), story_line, fill=text_color, font=text_book_font) # draw text
        top += font_height + 5
    
    del context # destroy drawing context
    img.save(filename + fileformat, "PNG")
    

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
