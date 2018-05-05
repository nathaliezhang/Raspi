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
            "C'est l'histoire de",
            "Il y a bien longtemps",
            "qui",
            "et",
            "Soudain",
            "Un jour",
            "Tout à coup",
            "montagne.",
            "champignons"
        ]
        
        # fonts
        maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
        maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'
        text_maison_neue_book = ImageFont.truetype(maison_neue_book, self.font_size, encoding="unic")
        text_maison_neue_bold = ImageFont.truetype(maison_neue_bold, self.font_size, encoding="unic")
        text_end_maison_neue_bold = ImageFont.truetype(maison_neue_bold, 100, encoding="unic")
        
        # multiline_text : text wrap
        self.text = story
        story_lines = textwrap.wrap(self.text, width=25)
        nb_lines = len(story_lines)
        font_width, font_height = text_maison_neue_book.getsize(self.text)
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
                    if strong == "montagne.":
                        if begin >= 0:
                            nb_lines += 1
                        mountains_img = Image.open("assets/img/mountains.jpg")
                        img_width, img_height = mountains_img.size
                        images_height += img_height
##                    if strong == "champignons":
##                        if begin >= 0:
##                            nb_lines += 1
##                        mushroom_img = Image.open("assets/img/mountains.jpg")
##                        img_width, img_height = mushroom_img.size
##                        images_height += img_height
                        
        # add end
        the_end = "FIN"
        the_end_width, the_end_height = text_maison_neue_book.getsize(the_end)
        
        height = 2 * top + nb_lines * spacing + images_height + the_end_height
        img = Image.new('L', (self.width, height), self.bg_color)
        context = ImageDraw.Draw(img) #create a drawing context

        
        for story_line in story_lines:
            show_sentence = 1
            
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
                    before_width, before_height = text_maison_neue_book.getsize(before) # get text width
                    context.multiline_text((left,top), before, fill=self.text_color, font=text_maison_neue_book) # draw text
                    left = left + before_width

                    strong = story_line[begin:end]
                    
##                    if strong == "champignons":
##                        if begin > 0: # pas le premier mot : retour à la ligne
##                            top += spacing
##                        #resize img if too big  
##                        old_img = Image.open("assets/img/mountains.jpg")
##                        img_width, img_height = old_img.size
##                        if img_width > 384:
##                            old_img = old_img.resize((384, (384*img_height)/img_width))
##                            old_img.save("assets/img/mountains.jpg")
##                            #open img
##                            new_img = Image.open("assets/img/mountains.jpg")
##                            img.paste(new_img, (0, top))
##                            img_width, img_height = new_img.size
##                            top += img_height
##                        else:
##                            img.paste(old_img, (0, top))
##                            top += img_height
                            
                    if strong == "montagne.":
                        #if begin > 0: # pas le premier mot : retour à la ligne
                            #top += spacing
                        #strong_width, strong_height = text_maison_neue_bold.getsize(strong)
                        #context.multiline_text((10,top), strong, fill=self.text_color, font=text_maison_neue_bold)
                        custom_img = Image.open("assets/img/mountains.jpg")
                        img.paste(custom_img, (10, top + strong_height))
                        #img.paste(custom_img, (10, top))
                        top += img_height
                    else:
                        strong_width, strong_height = text_maison_neue_bold.getsize(strong)
                        context.multiline_text((left,top), strong, fill=self.text_color, font=text_maison_neue_bold)
                    left = left + strong_width
                    
                    if end == len(story_line):
                        after = ""
                    else:
                        after = story_line[end:len(story_line)]
                    after_width, after_height = text_maison_neue_book.getsize(after)
                    context.multiline_text((left,top), after, fill=self.text_color, font=text_maison_neue_book)
                    break
                    
            if show_sentence == 1: #hasn't the expression
                context.text((left,top), story_line, fill=self.text_color, font=text_maison_neue_book) 
                
            top += spacing
        
        # add end
        the_end = "FIN"
        the_end_width, the_end_height = text_end_maison_neue_bold.getsize(the_end)
        center_text = (self.width - the_end_width) / 2
        list_the_end = list(the_end)
        for letter in list_the_end:
            if letter == "F":
                letter_width, letter_height = text_end_maison_neue_bold.getsize(letter)
                letter_img = Image.new('RGBA', (letter_width, letter_height), (255, 255, 255, 15))
                letter_ctx = ImageDraw.Draw(letter_img)
                letter_ctx.text((0,0), letter, fill=self.text_color, font=text_end_maison_neue_bold)
                rotate = letter_img.rotate(-15, expand=1)
                
                rotate_width, rotate_height = rotate.size
                resize = rotate.resize((50, (50*rotate_height)/rotate_width))
                
                img.paste(resize, (center_text, top))
                left = center_text + letter_width + 5
                top += 5
            if letter == "I":
                letter_width, letter_height = text_end_maison_neue_bold.getsize(letter)
                letter_img = Image.new('L', (letter_width, letter_height), self.bg_color)
                letter_ctx = ImageDraw.Draw(letter_img)
                letter_ctx.text((0,0), letter, fill=self.text_color, font=text_end_maison_neue_bold)
                rotate = letter_img.rotate(-5, expand=1)
                img.paste(rotate, (left, top))
                left = left + letter_width
                top += 5
            if letter == "N":
                letter_width, letter_height = text_end_maison_neue_bold.getsize(letter)
                letter_img = Image.new('L', (letter_width, letter_height), self.bg_color)
                letter_ctx = ImageDraw.Draw(letter_img)
                letter_ctx.text((0,0), letter, fill=self.text_color, font=text_end_maison_neue_bold)
                rotate = letter_img.rotate(15, expand=1)
                img.paste(rotate, (left, top))
                
        #context.text((center_text,top), the_end, fill=self.text_color, font=text_maison_neue_bold)
        
        del context # destroy drawing context
        img.save(self.filename + self.fileformat, "PNG")