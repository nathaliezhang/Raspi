#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageDraw, ImageFont
import textwrap
import sys
import effects
from random import randint

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
         self.font_size = 28
         self.text_color = "#000"
         self.custom_words = [
            "Il était une fois",
            "C'est l'histoire",
            "Il y a bien longtemps",
            "Un matin",
            "Soudain",
            "Tout à coup",
            "Brusquement",
            "Subitement",
            "Le lendemain",
            "Quelques heures plus tard",
            "Peu de temps après",
            "Puis",
            "Ensuite",
            "Peu après",
            "De temps en temps",
            "C'est alors",
            "Heureusement",
            "Malheureusement",
            "Et c'est ainsi",
            "Depuis ce jour",
            "Un jour",
            "Désormais"
        ]
    
    def text_in_img(self, title, story):
    
        in_part = False

        # fonts
        editor_regular = 'assets/fonts/Editor/Editor-Regular.ttf'
        editor_medium = 'assets/fonts/Editor/Editor-Medium.ttf'
        editor_bold = 'assets/fonts/Editor/Editor-Bold.ttf'
        maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
        maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'
        maison_neue_rotate = 'assets/fonts/Maison-Neue/Maison-Neue-Rotate.otf'
        maison_neue_rcontour = 'assets/fonts/Maison-Neue/Maison-Neue-RContour.otf'
        
        text_maison_neue_book = ImageFont.truetype(maison_neue_book, self.font_size, encoding="unic")
        text_maison_neue_bold = ImageFont.truetype(maison_neue_bold, self.font_size, encoding="unic")
        
        
        # multiline_text : text wrap
        self.text = story
        story_parts = story.split("@"); # detect new part of the story
        
        # init story params
        top = 0
        title_margin_bottom = 120
        font_width, font_height = text_maison_neue_book.getsize(self.text)
        spacing = font_height + 5
        before = bottom = 50
        after_part = 100
        
        onceupon_effect = randint(1,2)
        print onceupon_effect
        
        height = effects.get_img_height(self.custom_words, title, story_parts, self.width, onceupon_effect, top, spacing, title_margin_bottom, before, after_part, bottom)
        img = Image.new('L', (self.width, height), self.bg_color)
        context = ImageDraw.Draw(img) #create a drawing context
        

        # start to draw in the context
        
        # draw title
        title_lines = textwrap.wrap(title, width=28)
        top += before # space on the top of the paper
        for title_line in title_lines:
            custom_width, custom_height = text_maison_neue_bold.getsize(title_line) # get text width
            center_left = (self.width - custom_width) / 2; # center text
            context.text((center_left,top), title_line, fill=self.text_color, font=text_maison_neue_bold)
            top += spacing
        top += title_margin_bottom #space before part
            
	
	for index, story_part in enumerate(story_parts):
	    story_lines = textwrap.wrap(story_part, width=28)
	    
	    ordered_custom_words = self.get_part_custom_words(story_parts, index)
	    
	    # detect custom words
            for expression in ordered_custom_words:
                begin = story_part.find(expression)
		end = begin + len(expression)
		
		# custom words 
		start_sentence = story_part[begin:end + 1].strip() # space before @
		custom_width, custom_height = text_maison_neue_bold.getsize(start_sentence) # get text width
		center_left = (self.width - custom_width) / 2; # center text
		
		
		# check if have a custom word in this paragraph
		if start_sentence.find(",") >= 0:
		    start_sentence = start_sentence[0:len(start_sentence) - 1] # suctract "," to detect the word
		    
		    
		# fonction mirrot effect
		if start_sentence == "Il était une fois":
		    if onceupon_effect == 1:
			height = effects.two_fonts(self.width, start_sentence, editor_regular, self.font_size + 10, maison_neue_book, self.font_size - 4, spacing + 10, self.text_color, top, context)
		    elif onceupon_effect == 2:
			height = effects.mirror_font(self.width, start_sentence, editor_regular, self.font_size + 5, spacing -5, self.text_color, top, context)            
		    top += height
		    
		elif start_sentence == "Un jour" or start_sentence == 'Un matin':
		    effects.word_in_sentence(self.width, start_sentence, maison_neue_book, self.font_size, maison_neue_rotate, self.font_size + 25, self.text_color, top, context)
		   
		# fonction to increase text in uppercase and reduce font size if expression width > paper width
		elif start_sentence == "Tout à coup" or start_sentence == 'Soudain' or start_sentence == 'Brusquement' or start_sentence == 'Subitement':
		    font_size = self.font_size + 5
		    custom_width = effects.increase_font(start_sentence, editor_bold, font_size, self.text_color, top)
		    while custom_width > self.width:
                        custom_width = effects.increase_font(start_sentence, editor_bold, font_size, self.text_color, top)
                        font_size -= 1
		    center_left = (self.width - custom_width) / 2;
		    effects.increase_font(start_sentence, editor_bold, font_size, self.text_color, top, center_left, context)
		    top += 15
		    
		elif start_sentence == "Ensuite":
		    effects.line_between(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, context)
		
		elif start_sentence == "C'est alors":
		    height = effects.space_between(self.width, start_sentence, maison_neue_book, self.font_size, spacing - 25, self.text_color, top, context)
		    top += height
		
		elif start_sentence == "Heureusement":
		    height = effects.vertical_syllable_mirror(self.width, start_sentence, maison_neue_book, self.font_size, spacing, self.text_color, top, context)
		    top += height
		    
		elif start_sentence == "Malheureusement":
		    height = effects.decrease_syllale(self.width, start_sentence, maison_neue_book, self.font_size, spacing, self.text_color, top, context)
		    top += height
		     
                elif start_sentence == "De temps en temps":
                    left_one = effects.increase_decrease(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, 1)[0]
                    left_two = effects.increase_decrease(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, 2)[1]

                    height = effects.increase_decrease(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, 2)[2]
                    center_left_one = (self.width - left_one) / 2;
                    effects.increase_decrease(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, 1, center_left_one, context)
                    
                    center_left_two = (self.width - left_two) / 2;
                    effects.increase_decrease(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, 2, center_left_two, context)

                    top += height
                    
##                    elif start_sentence == "Puis":
##                        # create fonction to load img
##                        img_height = effects.add_image("assets/img/mountains.jpg", True, top, img)
##                        top += img_height
		    
		else :
		    context.text((center_left, top), start_sentence + ', ', fill=self.text_color, font=text_maison_neue_bold)
		top += spacing
		
		# the rest of the sentence
		end_sentence = story_part[end + 1:len(story_part)].strip()
		
		# has a custom word in the previous end_send that has a custom word
		for expression in ordered_custom_words:
		    if end_sentence.find(expression) >= 0: # if end_entence contain à custom word : cut
			 end_twice = end_sentence.find(expression)
			 end_sentence = end_sentence[0:end_twice].strip()
		
		# get the first sentence
		index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
		first_sentence = end_sentence[0:index_end_first_sentence + 1]
		rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
		
		# center first sentence end or not
		first_story_lines = textwrap.wrap(first_sentence, width=28)
		for first_story_line in first_story_lines:
		    
		    if start_sentence == "Soudain" or start_sentence == 'Tout à coup' or start_sentence == 'Brusquement' or start_sentence == 'Subitement':
			text_maison_neue_rotate = ImageFont.truetype(maison_neue_rotate, self.font_size + 5, encoding="unic")
			line_width, line_height = text_maison_neue_rotate.getsize(first_story_line) # get text width
			center_left = (self.width - line_width) / 2; # center text
			context.multiline_text((center_left, top), first_story_line, fill=self.text_color, font=text_maison_neue_rotate) # draw text
			top -= 5 
		    
		    elif start_sentence == "Un jour":
			left = effects.word_in_sentence(self.width, start_sentence, maison_neue_book, self.font_size, maison_neue_rotate, self.font_size + 25, self.text_color, top, False)
			top = effects.paragraph_after_effect(first_sentence, 20, left, top + 10, spacing, self.text_color, text_maison_neue_book, context, True)
			break
			
		    elif start_sentence == "Ensuite":
			left = effects.line_between(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, False)
			top = effects.paragraph_after_effect(first_sentence, 15, left, top, spacing, self.text_color, text_maison_neue_book, context)
			break                           
			
		    else:    
			line_width, line_height = text_maison_neue_book.getsize(first_story_line) # get text width
			center_left = (self.width - line_width) / 2; # center text
			context.multiline_text((center_left,top), first_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
		    top += spacing
		top += spacing - 10
		
		# rest of the part
		rest_story_lines = textwrap.wrap(rest_sentences, width=28)
		for rest_story_line in rest_story_lines:
		    line_width, line_height = text_maison_neue_book.getsize(rest_story_line) # get text width
		    context.multiline_text((0,top), rest_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
		    top += spacing
                    
            top += after_part
        
        del context # destroy drawing context
        img.save(self.filename + self.fileformat, "PNG")
        
        
    def get_part_custom_words (self, story_parts, num_part):
        
        custom_words = []
        positions = []
        ordered_words = []
        
        # get custom words that are in the story part
        for index, story_part in enumerate(story_parts):
            if index == num_part :
                for expression in self.custom_words:
                    begin = story_part.find(expression)
                    
                    if begin >= 0: #has the expression
                        positions.extend([begin, expression])
                        custom_words.append(positions)
                        positions = []
        
        # sort the custom words and their position according their appeareance in the story part
        custom_words = sorted(custom_words, key=lambda index: index[0])
        
        # ordered custom words
        for custom_word in custom_words:
            ordered_words.append(custom_word[1])

        return ordered_words
     
