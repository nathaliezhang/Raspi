#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageFont
import textwrap



# fonts
editor_regular = 'assets/fonts/Editor/Editor-Regular.ttf'
editor_medium = 'assets/fonts/Editor/Editor-Medium.ttf'
editor_bold = 'assets/fonts/Editor/Editor-Bold.ttf'
maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'

def get_img_height(custom_words, title, story_parts, width, onceupon_effect, top, spacing, title_margin_bottom, before_part, after_part, bottom):
        
    nb_lines = 0
    nb_parts = 0
    images_height = 0
    font_effects_height = 0
        
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
                
                if start_sentence == "Il était une fois":
                    if onceupon_effect == 1:
                        height = two_fonts(width, start_sentence, editor_regular, 35, maison_neue_book, 20, spacing + 10, "#000", top)
                    elif onceupon_effect == 2:
                        height = mirror_font(width, start_sentence, editor_regular, 30, spacing -5, "#000", top)            
                    font_effects_height += height
                        
##                # get the images height for drawImage
##                if start_sentence == "Puis":
##                    img_height = add_image("assets/img/mountains.jpg", False)
##                    images_height += img_height
                        
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
            
    height = top + title_margin_bottom + nb_lines * spacing + nb_parts * before_part + nb_parts * after_part + images_height + font_effects_height + bottom
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

    
def mirror_font(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    
    words = start_sentence.split(" ")
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    mirror_top = top
    height = 0
    
    for index, word in enumerate(words):
        if index % 2 == 0: # even
            word_width, word_height = text_font.getsize(word)
            left = width / 2
            if context : context.text((left,mirror_top), word, fill=text_color, font=text_font)
            mirror_top += spacing
            height += spacing
        else: # odd
            word_width, word_height = text_font.getsize(word)
            left = width / 2 - word_width
            if context : context.text((left,mirror_top), word, fill=text_color, font=text_font)
            mirror_top += spacing
            height += spacing
            
    return height


def two_fonts(width, start_sentence, first_font, first_font_size, second_font, second_font_size, spacing, text_color, top, context = False):
    effect_top = top
    height = 0
    
    first_text_font = ImageFont.truetype(first_font, first_font_size, encoding="unic")
    second_text_font = ImageFont.truetype(second_font, second_font_size, encoding="unic")
    
    words = start_sentence.split(" ", 2)
    part_one = (words[0] + ' ' + words[1]).upper()
    part_one_width, part_one_height = first_text_font.getsize(part_one)
    first_center_left = (width - part_one_width) / 2
    if context : context.text((first_center_left,effect_top), part_one, fill=text_color, font=first_text_font)
    effect_top += spacing
    height += spacing
    
    part_two = words[2].upper()
    part_two_width, part_two_height = second_text_font.getsize(part_two)
    second_center_left = (width - part_two_width) / 2
    if context : context.text((second_center_left,effect_top), part_two, fill=text_color, font=second_text_font)
    
    return height
            
    
def add_image(url, add, top = 0, img_bg = False):
    custom_img = Image.open(url)
    if add == True : img_bg.paste(custom_img, (0, top))
    img_width, img_height = custom_img.size
        
    return img_height