#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageDraw, ImageFont
import textwrap
import sys

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf8')

class StoryDesign():
    
    def __init__(self):
         self.text = ""
         self.filename = "assets/texts/story"
         self.fileformat = ".png"
         self.width = 384
         self.bg_color = "#FFF"
         self.font_size = 25
         self.text_color = "#000"
    
    def text_in_img(self, story):
        # highlight words
        custom_words = [
            "Il était une fois",
            "C'est l'histoire",
            "Il y a bien longtemps",
            "Soudain",
            "Un jour",
            "Tout à coup",
            "Le lendemain",
            "Quelques heures plus tard",
            "Peu de temps après",
        ]
        
        # fonts
        maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
        maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'
        text_maison_neue_book = ImageFont.truetype(maison_neue_book, self.font_size, encoding="unic")
        text_maison_neue_bold = ImageFont.truetype(maison_neue_bold, self.font_size, encoding="unic")
        text_end_maison_neue_bold = ImageFont.truetype(maison_neue_bold, 100, encoding="unic")
        
        # multiline_text : text wrap
        self.text = story
        
        story_parts = story.split("@"); # detect new part of the story 
        nb_lines = 0
        nb_parts = 0
        images_height = 0
        
        for story_part in story_parts: # nb parts
        
            # detect custom words
            for expression in custom_words:
                begin = story_part.find(expression)
                if begin >= 0: #has the expression
                    end = begin + len(expression)
                    
                    start_sentence = story_part[begin:end + 1].strip() # custom words
                    if start_sentence.find(","): start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
                    
                    # get the images height for drawImage
                    if start_sentence == "Quelques heures plus tard":
                        mountains_img = Image.open("assets/img/mountains.jpg")
                        img_width, img_height = mountains_img.size
                        images_height += img_height
                        
                    #rest of the sentence
                    end_sentence = story_part[end + 1:len(story_part)].strip()
                    
                    # get the first sentence
                    index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
                    first_sentence = end_sentence[0:index_end_first_sentence + 1]
                    rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
                    
                    first_story_lines = textwrap.wrap(first_sentence, width=32)
                    rest_story_lines = textwrap.wrap(rest_sentences, width=32)
                    
                    nb_lines += len(first_story_lines)
                    nb_lines += len(rest_story_lines)
            nb_lines += 1
            nb_parts += 1
            
        font_width, font_height = text_maison_neue_book.getsize(self.text)
        top = 0
        spacing = font_height + 5
        before_part = bottom = 60
        after_part = 30
        
        height = top + nb_lines * spacing + nb_parts * before_part + nb_parts * after_part + images_height + bottom
        print height
        img = Image.new('L', (self.width, height), self.bg_color)
        context = ImageDraw.Draw(img) #create a drawing context
        
        
        # start to draw in the context 
		
	for story_part in story_parts:
	    story_lines = textwrap.wrap(story_part, width=32)
	    
	    
	    # detect custom words
            for expression in custom_words:
                begin = story_part.find(expression)
                if begin >= 0: #has the expression
                    end = begin + len(expression)
                    
                    start_sentence = story_part[begin:end + 1].strip() # custom words
                    custom_width, custom_height = text_maison_neue_bold.getsize(start_sentence) # get text width
                    center_left = (self.width - custom_width) / 2; # center text
                    top += before_part #space before part
                    
                    # add images
                    if start_sentence.find(","): start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
                    if start_sentence == "Quelques heures plus tard":
                        custom_img = Image.open("assets/img/mountains.jpg")
                        img.paste(custom_img, (0, top))
                        img_width, img_height = custom_img.size
                        top += img_height    
                    else :
                        context.text((center_left,top), start_sentence, fill=self.text_color, font=text_maison_neue_bold)
                    top += spacing
                    
                    end_sentence = story_part[end + 1:len(story_part)].strip() # the rest of the sentence
                    
                    
                    # get the first sentence
                    index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
                    first_sentence = end_sentence[0:index_end_first_sentence + 1]
                    rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
                    
                    # center first sentence
                    first_story_lines = textwrap.wrap(first_sentence, width=32)
                    for first_story_line in first_story_lines:
                        line_width, line_height = text_maison_neue_book.getsize(first_story_line) # get text width
                        center_left = (self.width - line_width) / 2; # center text
                        context.multiline_text((center_left,top), first_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                        top += spacing
                    top += after_part
                    
                    # rest of the part
                    rest_story_lines = textwrap.wrap(rest_sentences, width=32)
                    for rest_story_line in rest_story_lines:
                        line_width, line_height = text_maison_neue_book.getsize(rest_story_line) # get text width
                        context.multiline_text((0,top), rest_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                        top += spacing
                    
        
        del context # destroy drawing context
        img.save(self.filename + self.fileformat, "PNG")
