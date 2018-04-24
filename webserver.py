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
	
	# run the command to print the image
	filename = "assets/texts/story"
	fileformat = ".png"
	width = 384
	bg_color = "#FFF"
	font_size = 25
	text_transform(story, filename, fileformat, width, bg_color, font_size)
	#os.system('lpr -o fit-to-page ' + filename + fileformat + '')
	#os.system('lpr ' + filename + fileformat + '')
	print story
	
	self.send_response(200) # return status
	self.send_header('Content-type','text/html') # return header
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
    
    custom_words = [
        "Il était une fois",
        "C'est l'histoire des",
        "Il y a bien longtemps",
        "qui",
        "et",
        "Soudain",
        "Un jour",
        "Tout à coup",
        "à la montagne."
    ]
    
    # fonts
    maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
    maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, font_size, encoding="unic")
    text_maison_neue_bold = ImageFont.truetype(maison_neue_bold, font_size, encoding="unic")
    
    # multiline_text : text wrap
    story_lines = textwrap.wrap(text, width=25)
    nb_lines = len(story_lines)
    font_width, font_height = text_maison_neue_book.getsize(text)
    top = 30
    spacing = font_height + 5
    images_height = 0
    # get the images height for drawImage
    for story_line in story_lines:
        for expression in custom_words:
            begin = story_line.find(expression)
            if begin >= 0: #has the expression
                end = begin + len(expression)
                strong = story_line[begin:end]
                if strong == "à la montagne.":
                    custom_img = Image.open("assets/img/mountains.jpg")
                    img_width, img_height = custom_img.size
                    images_height += img_height    
    height = 2 * top + nb_lines * spacing + images_height # img height : margin-top + text + margin-bottom
    img = Image.new('L', (width, height), bg_color)
    context = ImageDraw.Draw(img) #create a drawing context

    
    for story_line in story_lines:
        show_sentence = 1
        
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
                before = unicode(before, 'UTF-8') # encode text : correct before print
                before_width, before_height = text_maison_neue_book.getsize(before) # get text width
                context.multiline_text((left,top), before, fill=text_color, font=text_maison_neue_book) # draw text
                left = left + before_width

                strong = story_line[begin:end]
                
                if strong == "à la montagne.":
                    if begin > 0: # pas le premier mot : retour à la ligne
                        top += spacing
                    strong = unicode(strong, 'UTF-8').upper()
                    strong_width, strong_height = text_maison_neue_bold.getsize(strong)
                    context.multiline_text((10,top), strong, fill=text_color, font=text_maison_neue_bold)
                    custom_img = Image.open("assets/img/mountains.jpg")
                    img.paste(custom_img, (10, top + strong_height))
                    
                else:
                    strong = unicode(strong, 'UTF-8')
                    strong_width, strong_height = text_maison_neue_bold.getsize(strong)
                    context.multiline_text((left,top), strong, fill=text_color, font=text_maison_neue_bold)
                left = left + strong_width
                
                if end == len(story_line):
                    after = ""
                else:
                    after = story_line[end:len(story_line)]
                after = unicode(after, 'UTF-8')
                after_width, after_height = text_maison_neue_book.getsize(after)
                context.multiline_text((left,top), after, fill=text_color, font=text_maison_neue_book)
                break
                
        if show_sentence == 1: #hasn't the expression
            story_line = unicode(story_line, 'UTF-8')
            context.text((left,top), story_line, fill=text_color, font=text_maison_neue_book) 
            
        top += spacing
    
    del context # destroy drawing context
    img.save(filename + fileformat, "PNG")
    

# run only the function in this file and not in an import
if __name__ == '__main__':
    run()
