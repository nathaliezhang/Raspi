#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageDraw, ImageFont
import textwrap
import sys
import effects
from random import randint
import datetime

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf8')

class StoryDesign():
    
    end_random = randint(1,3)
    
    def __init__(self):
         self.text = ""
         self.filename = "assets/texts/story"
         self.fileformat = ".png"
         self.width = 384
         self.bg_color = "#FFF"
         self.font_size = 26
         self.text_color = "#000"
         self.intro_customs = [
             "Il était une fois", "Il y a bien longtemps", "Il fut un temps"]
         self.custom_words = [
            "Il était une fois", "Il y a bien longtemps", "Il fut un temps",
            "dans un coquillage", "au beau milieu d'un désert", "près d'une cascade", "sur la lune", "au coeur de la jungle", "à l'orée d'une forêt",
            "Soudain", "Tout à coup", "Brusquement", "Subitement",
            "C'est alors qu'un sorcier surgit de nulle part, tendit une cuillère avant de disparaitre à nouveau.",
            "C'est alors qu'un sorcier surgit de nulle part, il jeta un sort et éclata de rire.",
            "C'est alors que des météorites tombèrent du ciel. Elle créèrent d'énormes cratères en s'écrasant sur le sol !",
            "C'est alors que des météorites tombèrent du ciel. Elles roulèrent et enflammèrent tout ce qui se trouvait aux alentours.",
            "C'est alors qu'une tornade effroyable éclata. Le vent était si fort qu'il emportait tout sur son passage.",
            "C'est alors qu'une tornade effroyable éclata. Par chance, elle ne dura pas très longtemps.",
            "C'est alors qu'une guerrière apparut et proposa d'accompagner les personnages dans leur aventure.",
            "C'est alors qu'une guerrière apparut et lança un défi : réussir à la battre à l'épée.",
            "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! Le tronc était assez large pour grimper dessus.",
            "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! La plante gênait le passage.", 
            "Puis", "Ensuite",
            "De temps en temps",
            "Heureusement", "Malheureusement", "Finalement",
            "Et c'est ainsi", "Depuis ce jour", "Désormais",
            "Un jour", "Un matin"]
         self.imposed_events = [
             "C'est alors que des météorites tombèrent du ciel.",
             "C'est alors qu'une tornade effroyable éclata.",
             "C'est alors qu'une guerrière apparut",
             "C'est alors qu'un sorcier surgit de nulle part,",
             "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin !"]
        
    
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
        maison_neue_contour = 'assets/fonts/Maison-Neue/MaisonContour.otf'
        proto_grotesk_regular = 'assets/fonts/ProtoGrotesk/ProtoGrotesk-Regular.otf'
        proto_grotesk_bold = 'assets/fonts/ProtoGrotesk/ProtoGrotesk-Bold.otf'
        
        text_maison_neue_book = ImageFont.truetype(maison_neue_book, self.font_size, encoding="unic")
        text_maison_neue_bold = ImageFont.truetype(maison_neue_bold, self.font_size, encoding="unic")
        
        
        # multiline_text : text wrap
        self.text = story
        story_parts = story.split("@"); # detect new part of the story
        
        # init story params
        top = 0
        title_margin_bottom = 80
        font_width, font_height = text_maison_neue_book.getsize(self.text)
        spacing = font_height + 5
        before = bottom = 100
        after_part = 80
        
        onceupon_effect = randint(1,2)
        print onceupon_effect
        
        height = effects.get_img_height(self.custom_words, title, story_parts, self.width, onceupon_effect, top, spacing, title_margin_bottom, before, after_part, bottom)
        img = Image.new('L', (self.width, height), self.bg_color)
        context = ImageDraw.Draw(img) #create a drawing context
        

        # START TO DRAW IN THE CONTEXT
        
        # draw title
        top += before # space on the top of the paper
        height = effects.two_fonts_title(self.width, title, proto_grotesk_regular, proto_grotesk_bold, spacing, self.text_color, top, context)
        top += height + title_margin_bottom #space before part
        
        top_end = 0
	
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
		    
		elif start_sentence == "Il y a bien longtemps":
                    height = effects.two_fonts(self.width, start_sentence, editor_regular, self.font_size + 10, maison_neue_book, self.font_size - 4, spacing + 10, self.text_color, top, context)
                    top += height
                    
                elif start_sentence == "au beau milieu d'un désert.":
                                    
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                            
                    # place in the sentence
                    words = start_sentence.split(" ")
                    space = 30 * self.width / 100
                    for word in words:
                        context.text((left,top - spacing), word, fill=self.text_color, font=text_maison_neue_book)
                        left += space
                        word_width, word_height = text_maison_neue_book.getsize(word)
                        if (left + word_width) > self.width:
                            left = 0
                            top += spacing
                    top -= 2 * spacing
                            
                elif start_sentence == "à l'orée d'une forêt.":
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                    effects.place_img_position(self.width, start_sentence, spacing, self.font_size, self.text_color, top, left, context, img)
                    top += 30
                
                elif start_sentence == "au coeur de la jungle.":
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                    effects.place_img_position(self.width, start_sentence, spacing, self.font_size, self.text_color, top, left, context, img)
                    top += 30
                
                elif start_sentence == "près d'une cascade.":
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                    effects.place_img_position(self.width, start_sentence, spacing, self.font_size, self.text_color, top, left, context, img)
                    top += 80
                
                elif start_sentence == "sur la lune.":
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                    effects.place_img_position(self.width, start_sentence, spacing, self.font_size, self.text_color, top, left, context, img)
                
                elif start_sentence == "dans un coquillage.":
                    left = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[0]
                    top = effects.get_left_place(self.width, start_sentence, story_part, top, self.font_size, spacing)[1]
                    effects.place_img_position(self.width, start_sentence, spacing, self.font_size, self.text_color, top, left, context, img)
                    
		    
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
		    
		elif start_sentence == "C'est alors qu'un sorcier surgit de nulle part, tendit une cuillère avant de disparaitre à nouveau" or start_sentence == "C'est alors qu'un sorcier surgit de nulle part, il jeta un sort et éclata de rire":
                    height = effects.imposed_event(self.width, start_sentence, "sorcier", top, maison_neue_bold, maison_neue_contour, self.font_size, after_part, spacing, self.text_color, context)
		    top += height
		
		elif start_sentence == "C'est alors que des météorites tombèrent du ciel. Elle créèrent d'énormes cratères en s'écrasant sur le sol !" or start_sentence == "C'est alors que des météorites tombèrent du ciel. Elles roulèrent et enflammèrent tout ce qui se trouvait aux alentours.":
                    height = effects.imposed_event(self.width, start_sentence, "météorites", top, maison_neue_bold, maison_neue_contour, self.font_size, after_part, spacing, self.text_color, context)
		    top += height
		    
		elif start_sentence == "C'est alors qu'une tornade effroyable éclata. Le vent était si fort qu'il emportait tout sur son passage" or start_sentence == "C'est alors qu'une tornade effroyable éclata. Par chance, elle ne dura pas très longtemps":
                    height = effects.imposed_event(self.width, start_sentence, "tornade", top, maison_neue_bold, maison_neue_contour, self.font_size, after_part, spacing, self.text_color, context)
		    top += height
		    
                elif start_sentence == "C'est alors qu'une guerrière apparut et proposa d'accompagner les personnages dans leur aventure." or start_sentence == "C'est alors qu'une guerrière apparut et lança un défi : réussir à la battre à l'épée.":
                    height = effects.imposed_event(self.width, start_sentence, "guerrière", top, maison_neue_bold, maison_neue_contour, self.font_size, after_part, spacing, self.text_color, context)
		    top += height
		    
		elif start_sentence == "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! Le tronc était assez large pour grimper dessus." or start_sentence == "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! La plante gênait le passage.":
                    height = effects.imposed_event(self.width, start_sentence, "plante", top, maison_neue_bold, maison_neue_contour, self.font_size, after_part, spacing, self.text_color, context)
		    top += height
		    
                elif start_sentence == "Puis":
                    context.text((0, top), start_sentence, fill=self.text_color, font=text_maison_neue_book) # draw text
                
		elif start_sentence == "Ensuite":
		    effects.line_between(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, context)
		
##		elif start_sentence == "C'est alors":
##		    height = effects.space_between(self.width, start_sentence, maison_neue_book, self.font_size, spacing - 25, self.text_color, top, context)
##		    top += height
		
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
                    
                    
                elif start_sentence == "Depuis ce jour":
                    height = effects.since(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, context)
                    top += height
                    
                elif start_sentence == "Désormais":
                    height = effects.random_height(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, context)
                    top += height
                    
                elif start_sentence == "Et c'est ainsi":
                    context.text((0, top), start_sentence, fill=self.text_color, font=text_maison_neue_bold)
                
                elif start_sentence == "Il fut un temps":
                    context.text((0, top), start_sentence + ', ', fill=self.text_color, font=text_maison_neue_bold)
                    
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
			#top -= 5
                    elif start_sentence == "Il était une fois" or start_sentence == "Il y a bien longtemps" :
                        first_story_lines = textwrap.wrap(first_sentence, width=28)
                        for index, first_story_line in enumerate(first_story_lines):
                            line_width, line_height = text_maison_neue_book.getsize(first_story_line) # get text width
                            context.multiline_text((0,top), first_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                            if index == len(first_story_lines) - 1:
                                top += 2 * spacing / 5
                            else:
                                top += spacing
                        break
                    
                    elif start_sentence == "Il fut un temps":
                        word_width, word_height = text_maison_neue_bold.getsize(start_sentence + " ") # get text width
			top = effects.paragraph_after_effect(first_sentence, 15, word_width + 10, top, spacing, self.text_color, text_maison_neue_book, context)
			top -= 3 * spacing / 5
			break
		    elif start_sentence == "Un jour":
			left = effects.word_in_sentence(self.width, start_sentence, maison_neue_book, self.font_size, maison_neue_rotate, self.font_size + 25, self.text_color, top, False)
			top = effects.paragraph_after_effect(first_sentence, 20, left, top + 10, spacing, self.text_color, text_maison_neue_book, context, True)
			break
		    elif start_sentence == "Ensuite":
			left = effects.line_between(self.width, start_sentence, maison_neue_bold, self.font_size, spacing, self.text_color, top, False)
			top = effects.paragraph_after_effect(first_sentence, 15, left + 10, top, spacing, self.text_color, text_maison_neue_book, context)
			break
		    elif start_sentence == "Puis":
                        word_width, word_height = text_maison_neue_book.getsize(start_sentence + " ") # get text width
			top = effects.paragraph_after_effect(first_sentence, 28, word_width, top, spacing, self.text_color, text_maison_neue_book, context)
			break
		    elif start_sentence == "De temps en temps":
			top = effects.paragraph_after_effect(first_sentence, 28, 0, top + spacing, spacing, self.text_color, text_maison_neue_book, context) - 2 * spacing / 3
			break
		    elif start_sentence == "Malheureusement":
                        word_width, word_height = text_maison_neue_book.getsize(start_sentence.upper() + ",") # get text width
			top = effects.paragraph_after_effect(first_sentence, 10, word_width, top + spacing, spacing, self.text_color, text_maison_neue_book, context) - 2 * spacing / 3
			break
		    elif start_sentence == "Heureusement":
                        word_width, word_height = text_maison_neue_book.getsize(start_sentence.upper() + ",") # get text width
			top = effects.paragraph_after_effect(first_sentence, 15, word_width, top + spacing, spacing, self.text_color, text_maison_neue_book, context) - 2 * spacing / 3
			break
                    elif start_sentence == "Depuis ce jour":
                        word_width, word_height = text_maison_neue_bold.getsize(start_sentence.upper()) # get text width
			top = effects.paragraph_after_effect(first_sentence, 10, word_width - 15, top - spacing, spacing, self.text_color, text_maison_neue_book, context) - 2 * spacing / 3
			break
                    elif start_sentence == "Désormais":
                        word_width, word_height = text_maison_neue_bold.getsize(start_sentence.upper()) # get text width
			top = effects.paragraph_after_effect(first_sentence, 15, word_width + 20, top - 2 * spacing / 3, spacing, self.text_color, text_maison_neue_book, context) - 2 * spacing / 3
                        break
                    elif start_sentence == "Et c'est ainsi":
                        word_width, word_height = text_maison_neue_bold.getsize(start_sentence + " ") # get text width
                        top = effects.paragraph_after_effect(first_sentence, 15, word_width + 5, top, spacing, self.text_color, text_maison_neue_book, context)
                        print rest_sentences
                        break
                    
                        context.text((0, top), start_sentence, fill=self.text_color, font=text_maison_neue_bold)
		    else:    
			line_width, line_height = text_maison_neue_book.getsize(first_story_line) # get text width
			center_left = (self.width - line_width) / 2; # center text
			context.multiline_text((center_left,top), first_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
		    top += spacing
		    
		if start_sentence == "Soudain" or start_sentence == 'Tout à coup' or start_sentence == 'Brusquement' or start_sentence == 'Subitement':
                    top += after_part
                else:
                    top += spacing - 10
             
	
                rest_story_lines = textwrap.wrap(rest_sentences, width=28)
                for rest_story_line in rest_story_lines:
                    line_width, line_height = text_maison_neue_book.getsize(rest_story_line) # get text width
                    context.multiline_text((0,top), rest_story_line, fill=self.text_color, font=text_maison_neue_book) # draw text
                    top += spacing
		    
            top_end = self.get_value(top) # get top value   
            top += after_part

        # add end
        top_end += 30
        img_end_height = effects.add_image("assets/img/fin0"+ str(self.end_random) +".jpg", True, top_end, img)
        top_end += img_end_height
        
        height = effects.draw_end(self.width, top_end, font_size, self.text_color, spacing, img, context)

        
        del context # destroy drawing context
        img.save(self.filename + self.fileformat, "PNG")
        
        #img.rotate(180).save(self.filename + self.fileformat, "PNG")
        
        
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
    
    
    # get top value in a loop
    def get_value (self, top):
        return top
     
