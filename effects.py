#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageFont
import textwrap

def get_img_height(custom_words, title, story_parts, top, spacing, title_margin_bottom, before_part, after_part, bottom):
        
    nb_lines = 0
    nb_parts = 0
    images_height = 0
        
    # height according the title
    title_lines = textwrap.wrap(title, width=30)
    nb_lines += len(title_lines)
        
    for story_part in story_parts: # nb parts
    
        # detect custom words
        for expression in custom_words:
            begin = story_part.find(expression)
            if begin >= 0: #has the expression
                end = begin + len(expression)
                    
                start_sentence = story_part[begin:end + 1].strip() # custom words
                if start_sentence.find(","): start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
                    
                # get the images height for drawImage
                if start_sentence == "Puis":
                    img_height = add_image("assets/img/mountains.jpg", False)
                    images_height += img_height
                        
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
            
    height = top + title_margin_bottom + nb_lines * spacing + nb_parts * before_part + nb_parts * after_part + images_height + bottom
    return height
            
    
def increase_font(context, custom_word, font, font_size, text_color, top, left = 0):
        
    custom_word = custom_word.upper()
    word_letters = list(custom_word)
    increase_top = top
    center_left = left
    for letter in word_letters:
        text_font = ImageFont.truetype(font, font_size, encoding="unic")
        letter_width, letter_height = text_font.getsize(letter) # redo after uppercase center text
        if center_left != 0: # draw only if left is not null
            context.text((left,increase_top), letter, fill=text_color, font=text_font)
        left += letter_width
        increase_top -= int(round(font_size * .1))
        font_size += int(round(font_size * .1))
            
    return left #return the width
    
    
    
def add_image(url, add, top = 0, img_bg = False):
    custom_img = Image.open(url)
    if add == True : img_bg.paste(custom_img, (0, top))
    img_width, img_height = custom_img.size
        
    return img_height