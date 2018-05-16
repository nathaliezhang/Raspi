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

def get_img_height(custom_words, title, story_parts, width, onceupon_effect, top, spacing, title_margin_bottom, before, after_part, bottom):
        
    nb_lines = 0
    nb_parts = 0
    nb_subparts = 0
    images_height = 0
    font_effects_height = 0
        
    # height according the title
    title_lines = textwrap.wrap(title, width=28)
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
                
                elif start_sentence == "Tout à coup" or start_sentence == 'Soudain':
                    font_effects_height += spacing * 2 + 15
                    
                elif start_sentence == "C'est alors":
                    height = effects.space_between(self.width, start_sentence, maison_neue_book, 25, spacing - 25, self.text_color, top, context)
                    font_effects_height += height
                        
                elif start_sentence == "Ensuite":
                    font_effects_height += spacing
                        
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
                        rest_end_sentence = textwrap.wrap(end_sentence, width=28)
                        nb_lines += len(rest_end_sentence)
                        nb_subparts += 1
                        break
                    
                # get the first sentence
                index_end_first_sentence = end_sentence.find('.', 0, len(end_sentence))
                first_sentence = end_sentence[0:index_end_first_sentence + 1]
                rest_sentences = end_sentence[index_end_first_sentence + 1:len(end_sentence)].strip()
                    
                first_story_lines = textwrap.wrap(first_sentence, width=28)
                rest_story_lines = textwrap.wrap(rest_sentences, width=28)
                    
                nb_lines += len(first_story_lines)
                nb_lines += len(rest_story_lines)
        nb_lines += 1
        nb_parts += 1
    
    
    height = top + before + title_margin_bottom + nb_lines * spacing + nb_parts * after_part + images_height + font_effects_height + bottom - nb_subparts * (after_part - spacing) - after_part + spacing
    return height
            
    
def increase_font(custom_word, font, font_size, text_color, top, left = 0, context = False):
        
    custom_word = custom_word.upper()
    word_letters = list(custom_word)
    baseline = increase_top = top
    center_left = left
    for letter in word_letters:
        text_font = ImageFont.truetype(font, font_size, encoding="unic")
        letter_width, letter_height = text_font.getsize(letter) # redo after uppercase center text
        if center_left != 0: # draw only if left is not null
            if context : context.text((left,increase_top), letter, fill=text_color, font=text_font)
        left += letter_width
        increase_top -= int(round(font_size * .1))
        font_size += int(round(font_size * .1))
    
    # add comma
    baseline += int(round(font_size * .1))
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
    if context : context.text((left, baseline), ', ', fill=text_color, font=text_maison_neue_book)
    
    return left

    
def mirror_font(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    
    words = start_sentence.split(" ")
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    effect_top = top
    height = 0
    last_elm_left = 0
    
    for index, word in enumerate(words):
        if index % 2 == 0: # even
            word_width, word_height = text_font.getsize(word)
            left = width / 2
            if context : context.text((left,effect_top), word, fill=text_color, font=text_font)
            effect_top += spacing
            height += spacing
            if index == len(words) -1: last_elm_left = left + word_width
            
        else: # odd
            word_width, word_height = text_font.getsize(word)
            left = width / 2 - word_width
            if context : context.text((left,effect_top), word, fill=text_color, font=text_font)
            effect_top += spacing
            height += spacing
            if index == len(words) -1: last_elm_left = left + word_width
            
        if index == len(words) -1 : # add comma
            text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
            if context : context.text((last_elm_left, effect_top - 14), ', ', fill=text_color, font=text_maison_neue_book)
    
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
    
    # add comma
    comma_left = second_center_left + part_two_width
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
    if context : context.text((comma_left, effect_top - 2), ', ', fill=text_color, font=text_maison_neue_book)
            
    return height


def space_between(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    effect_top = top
    height = 0
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    
    words = start_sentence.upper().split(" ")
    if len(words) == 2:
        if context : context.text((0,effect_top), words[0], fill=text_color, font=text_font) # first word
        part_two_width, part_two_height = text_font.getsize(words[1]) # second word
        part_two_left = width - part_two_width
        if context : context.text((part_two_left,effect_top), words[1], fill=text_color, font=text_font)
        height += spacing
        
    return height


def word_in_sentence(width, start_sentence, first_font, first_font_size, second_fond, second_font_size, text_color, top, context = False):
    
    text_first_font = ImageFont.truetype(first_font, first_font_size, encoding="unic")
    text_second_font = ImageFont.truetype(second_fond, second_font_size, encoding="unic")
                        
    words = start_sentence.split(" ")
    if len(words) == 2:
        # first word
        first_word_width, first_word_height = text_first_font.getsize(words[0] + ' ') # get text width
        if context : context.text((0,top), words[0], fill=text_color, font=text_first_font) # draw text
                            
        # second word
        second_word_width, second_word_height = text_second_font.getsize(words[1]) # get text width
        if context : context.text((first_word_width,top - 35), words[1], fill=text_color, font=text_second_font) # draw text
        left = first_word_width + second_word_width
        
    return left

                            
def line_between(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    effect_top = top
    left = 0
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
                        
    if start_sentence == "Ensuite":
        
        start = start_sentence[0:2]
        end = start_sentence[2:len(start_sentence)] + ", "
        
        line_width = 100
        line_margin = 2
        start_width, start_height = text_font.getsize(start) # start word size
        end_width, end_height = text_font.getsize(end) # start word size
        line_start = start_width + line_margin
        
        if context:
            context.text((0, effect_top), start, fill=text_color, font=text_font) # en
            effect_top += font_size / 2
            context.line((line_start , effect_top, line_start + line_width, effect_top), "#000", 2) # line
            line_start += line_margin + line_width
            effect_top -= font_size / 2
            context.text((line_start, effect_top), end, fill=text_color, font=text_font) # suite
        
        left += start_width + line_margin * 2 + line_width + end_width
                            
    return left

    
def paragraph_after_effect(first_sentence, first_line_width, left, top, spacing, text_color, text_font, context, add_comma = False):
    
    effect_top = top
    sentences = textwrap.wrap(first_sentence, width=first_line_width)
                      
    if add_comma : first_part = ', ' + sentences[0]
    else : first_part = sentences[0]
    context.text((left, effect_top - spacing), first_part, fill=text_color, font=text_font)
                            
    rest_part = first_sentence[len(sentences[0]):len(first_sentence)].strip()
    rest_lines = textwrap.wrap(rest_part, width=28)
    for rest_line in rest_lines:
        context.text((0, effect_top), rest_line, fill=text_color, font=text_font)
        effect_top += spacing
    
    return effect_top

                    
def add_image(url, add, top = 0, img_bg = False):
    custom_img = Image.open(url)
    if add == True : img_bg.paste(custom_img, (0, top))
    img_width, img_height = custom_img.size
        
    return img_height