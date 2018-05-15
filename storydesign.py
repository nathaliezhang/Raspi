#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageDraw, ImageFont
import textwrap
import sys
import effects

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
         self.custom_words = [
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
    
    def text_in_img(self, title, story):

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
        
        # init story params
        top = 0
        title_margin_bottom = 60
        font_width, font_height = text_maison_neue_book.getsize(self.text)
        spacing = font_height + 5
        before_part = bottom = 60
        after_part = 30
        
        height = effects.get_img_height(self.custom_words, title, story_parts, top, spacing, title_margin_bottom, before_part, after_part, bottom)
        img = Image.new('L', (self.width, height), self.bg_color)
        context = ImageDraw.Draw(img) #create a drawing context
        
        
        # start to draw in the context
        
        # draw title
        title_lines = textwrap.wrap(title, width=30)
        for title_line in title_lines:
            custom_width, custom_height = text_maison_neue_bold.getsize(title_line) # get text width
            center_left = (self.width - custom_width) / 2; # center text
            top += before_part #space before part
            context.text((center_left,top), title_line, fill=self.text_color, font=text_maison_neue_bold)
            top += spacing
            
		
	for story_part in story_parts:
	    story_lines = textwrap.wrap(story_part, width=30)
	    
	    
	    # detect custom words
            for expression in self.custom_words:
                begin = story_part.find(expression)
                if begin >= 0: #has the expression
                    end = begin + len(expression)
                    
                    # custom words 
                    start_sentence = story_part[begin:end + 1].strip() # space before @
                    custom_width, custom_height = text_maison_neue_bold.getsize(start_sentence) # get text width
                    center_left = (self.width - custom_width) / 2; # center text
                    top += title_margin_bottom #space before part
                    
                    #TODO : Check if have a custom word in this paragraph
                    if start_sentence.find(",") >= 0:
                        start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
                        
                    # fonction mirrot effect
                    #if start_sentence == "Il était une fois":
                        
                       
                    # fonction to increase text in uppercase
                    if start_sentence == "Tout à coup" or start_sentence == 'Soudain':
                        custom_width = effects.increase_font(context, start_sentence, editor_bold, 25, self.text_color, top)
                        center_left = (self.width - custom_width) / 2;
                        effects.increase_font(context, start_sentence, editor_bold, 25, self.text_color, top, center_left)
                        
                    elif start_sentence == "Puis":
                        
                        # create fonction to load img
                        img_height = effects.add_image("assets/img/mountains.jpg", True, top, img)
                        top += img_height
                        
                    else :
                        context.text((center_left,top), start_sentence, fill=self.text_color, font=text_maison_neue_bold)
                    top += spacing
                    
                    # the rest of the sentence
                    end_sentence = story_part[end + 1:len(story_part)].strip()
                    
                    # TODO : case if there three custom words
                    # has a custom word in the previous end_send that has a custom word
                    for expression in self.custom_words:
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
     
