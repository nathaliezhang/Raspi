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
    
    def text_in_img(self, title, story):
        # highlight words
        custom_words = [
            "Il était une fois",
            "C'est l'histoire",
            "Il y a bien longtemps",
            "Un jour",
            "Soudain",
            "Tout à coup",
            "Le lendemain",
            "Quelques heures plus tard",
            "Peu de temps après",
            "Puis",
            "Ensuite",
            "Peu après",
            "Et c'est ainsi",
            "Depuis ce jour",
            "Désormais"
        ]
        
        # fonts
        editor_bold = 'assets/fonts/Editor/Editor-Bold.ttf'
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
##                    if start_sentence == "Quelques heures plus tard":
##                        img_height = self.add_image("assets/img/mountains.jpg", False)
##                        images_height += img_height
                        
                    #rest of the sentence
                    end_sentence = story_part[end + 1:len(story_part)].strip()
                    
                    # has a custom word in the previous end_send that has a custom word
                    for expression in custom_words:
                        if end_sentence.find(expression) >= 0: # if end_entence contain à custom word : cut
                            end_twice = end_sentence.find(expression)
                            end_sentence = end_sentence[0:end_twice].strip()
                            rest_end_sentence = textwrap.wrap(end_sentence, width=30)
                            nb_lines += len(rest_end_sentence)
                            break
                    
                    # get the first sentence
                    index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
                    first_sentence = end_sentence[0:index_end_first_sentence + 1]
                    rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
                    
                    first_story_lines = textwrap.wrap(first_sentence, width=30)
                    rest_story_lines = textwrap.wrap(rest_sentences, width=30)
                    
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
	    story_lines = textwrap.wrap(story_part, width=30)
	    
	    
	    # detect custom words
            for expression in custom_words:
                begin = story_part.find(expression)
                if begin >= 0: #has the expression
                    end = begin + len(expression)
                    
                    # custom words 
                    start_sentence = story_part[begin:end + 1].strip() # space before @
                    print start_sentence
                    custom_width, custom_height = text_maison_neue_bold.getsize(start_sentence) # get text width
                    center_left = (self.width - custom_width) / 2; # center text
                    top += before_part #space before part
                    
                    #TODO : Check if have a custom word in this paragraph
                    if start_sentence.find(",") >= 0:
                        start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
                       
                    # fonction to increase text in uppercase
                    if start_sentence == "Tout à coup" or start_sentence == 'Soudain':
                        custom_width = self.increase_font(context, start_sentence, editor_bold, 25, top)
                        center_left = (self.width - custom_width) / 2;
                        self.increase_font(context, start_sentence, editor_bold, 25, top, center_left)
                        
##                    elif start_sentence == "Quelques heures plus tard":
##                        
##                        # create fonction to load img
##                        img_height = self.add_image("assets/img/mountains.jpg", True, top, img)
##                        top += img_height
                        
                    else :
                        context.text((center_left,top), start_sentence, fill=self.text_color, font=text_maison_neue_bold)
                    top += spacing
                    
                    # the rest of the sentence
                    end_sentence = story_part[end + 1:len(story_part)].strip()
                    
                    # TODO : case if there three custom words
                    # has a custom word in the previous end_send that has a custom word
                    for expression in custom_words:
                        if end_sentence.find(expression) >= 0: # if end_entence contain à custom word : cut
                            end_twice = end_sentence.find(expression)
                            end_sentence = end_sentence[0:end_twice].strip()
                            break
                    
                    # get the first sentence
                    index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
                    first_sentence = end_sentence[0:index_end_first_sentence + 1]
                    rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
                    
                    # center first sentence
                    first_story_lines = textwrap.wrap(first_sentence, width=30)
                    for first_story_line in first_story_lines:
                        line_width, line_height = text_maison_neue_book.getsize(first_story_line) # get text width
                        center_left = (self.width - line_width) / 2; # center text
                        context.multiline_text((center_left,top), first_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                        top += spacing
                    top += after_part
                    
                    # rest of the part
                    rest_story_lines = textwrap.wrap(rest_sentences, width=30)
                    for rest_story_line in rest_story_lines:
                        line_width, line_height = text_maison_neue_book.getsize(rest_story_line) # get text width
                        context.multiline_text((0,top), rest_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                        top += spacing
                    
        
        del context # destroy drawing context
        img.save(self.filename + self.fileformat, "PNG")
        
    
    def increase_font(self, context, custom_word, font, font_size, top, left = 0):
        
        custom_word = custom_word.upper()
        word_letters = list(custom_word)
        increase_top = top
        center_left = left
        for letter in word_letters:
            text_font = ImageFont.truetype(font, font_size, encoding="unic")
            letter_width, letter_height = text_font.getsize(letter) # redo after uppercase center text
            if center_left != 0: # draw only if left is not null
                context.text((left,increase_top), letter, fill=self.text_color, font=text_font)
            left += letter_width
            increase_top -= int(round(font_size * .1))
            font_size += int(round(font_size * .1))
            
        return left #return the width
    
    
    
    def add_image(self, url, add, top = 0, img_bg = False):
        custom_img = Image.open(url)
        if add == True : img_bg.paste(custom_img, (0, top))
        img_width, img_height = custom_img.size
        
        return img_height
     
