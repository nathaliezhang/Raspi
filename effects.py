#!/usr/bin/env python
# coding: utf8

from PIL import Image, ImageFont
import textwrap
import storydesign
from random import randint
import re

# fonts
editor_regular = 'assets/fonts/Editor/Editor-Regular.ttf'
editor_medium = 'assets/fonts/Editor/Editor-Medium.ttf'
editor_bold = 'assets/fonts/Editor/Editor-Bold.ttf'
maison_neue_book = 'assets/fonts/Maison-Neue/Maison Neue Book.otf'
maison_neue_bold = 'assets/fonts/Maison-Neue/Maison Neue Bold.otf'
maison_neue_contour = 'assets/fonts/Maison-Neue/MaisonContour.otf'
proto_grotesk_regular = 'assets/fonts/ProtoGrotesk/ProtoGrotesk-Regular.otf'
proto_grotesk_bold = 'assets/fonts/ProtoGrotesk/ProtoGrotesk-Bold.otf'

def get_img_height(custom_words, title, story_parts, width, onceupon_effect, top, spacing, title_margin_bottom, before, after_part, bottom):
    
    paper = storydesign.StoryDesign()
    nb_lines = 0
    nb_parts = 0
    nb_subparts = 0
    images_height = 0
    font_effects_height = 0
        
    # height according the title
    title_lines = textwrap.wrap(title, width=28)
    nb_lines += len(title_lines)
        
    for index, story_part in enumerate(story_parts): # nb parts
       
        # detect custom words
        ordered_custom_words = paper.get_part_custom_words (story_parts, index)
        
        for expression in ordered_custom_words:
            begin = story_part.find(expression)
            end = begin + len(expression)
            start_sentence = story_part[begin:end + 1].strip() # custom word
            
            if start_sentence.find(","): start_sentence = start_sentence[0:len(start_sentence) - 1] #suctract ,
            
            if start_sentence == "Il était une fois":
                if onceupon_effect == 1:
                    height = two_fonts(width, start_sentence, editor_regular, 35, maison_neue_book, 20, spacing + 10, "#000", top)
                elif onceupon_effect == 2:
                    height = mirror_font(width, start_sentence, editor_regular, 30, spacing -5, "#000", top)            
                font_effects_height += height
            
            elif start_sentence == "Tout à coup" or start_sentence == 'Soudain':
                font_effects_height += spacing * 2 + 15
                
##            elif start_sentence == "C'est alors":
##                height = effects.space_between(width, start_sentence, maison_neue_book, 25, spacing - 25, "#000", top, context)
##                font_effects_height += height + 5
                
            elif start_sentence == "Un jour":
                font_effects_height += spacing + 10
                
            elif start_sentence == "Ensuite":
                font_effects_height += spacing
            
            elif start_sentence == "Malheureusement":
                height = decrease_syllale(width, start_sentence, maison_neue_book, 28, spacing, "#000", top)
                font_effects_height += height
                
            elif start_sentence == "De temps en temps":
                height = increase_decrease(width, start_sentence, maison_neue_bold, 28, spacing, "#000", top, 2)[2]
                font_effects_height += height
            
            elif start_sentence == "Depuis ce jour":
                height = since(width, start_sentence, maison_neue_bold, 28, spacing, "#000", top)
                font_effects_height += height
                
            elif start_sentence == "C'est alors qu'un sorcier surgit de nulle part, tendit une cuillère avant de disparaitre à nouveau" or start_sentence == "C'est alors qu'un sorcier surgit de nulle part, il jeta un sort et éclata de rire":
                height = imposed_event(width, start_sentence, "sorcier", top, maison_neue_bold, maison_neue_contour, 28, after_part, spacing, "#000")
		font_effects_height += height
		
	    elif start_sentence == "C'est alors que des météorites tombèrent du ciel. Elle créèrent d'énormes cratères en s'écrasant sur le sol !" or start_sentence == "C'est alors que des météorites tombèrent du ciel. Elles roulèrent et enflammèrent tout ce qui se trouvait aux alentours.":
                height = imposed_event(width, start_sentence, "météorites", top, maison_neue_bold, maison_neue_contour, 28, after_part, spacing,"#000")
		font_effects_heighttop += height
		    
	    elif start_sentence == "C'est alors qu'une tornade effroyable éclata. Le vent était si fort qu'il emportait tout sur son passage" or start_sentence == "C'est alors qu'une tornade effroyable éclata. Par chance, elle ne dura pas très longtemps":
                height = imposed_event(width, start_sentence, "tornade", top, maison_neue_bold, maison_neue_contour, 28, after_part, spacing, "#000")
		font_effects_height += height
		    
            elif start_sentence == "C'est alors qu'une guerrière apparut et proposa d'accompagner les personnages dans leur aventure." or start_sentence == "C'est alors qu'une guerrière apparut et lança un défi : réussir à la battre à l'épée.":
                height = imposed_event(width, start_sentence, "guerrière", top, maison_neue_bold, maison_neue_contour, 28, after_part, spacing, "#000")
		font_effects_height += height
		    
	    elif start_sentence == "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! Le tronc était assez large pour grimper dessus." or start_sentence == "C'est alors qu'une plante se mit à pousser tellement haut qu'on en voyait plus la fin ! La plante gênait le passage.":
                height = imposed_event(width, start_sentence, "plante", top, maison_neue_bold, maison_neue_contour, 28, after_part, spacing, "#000")
		font_effects_height += height
                    
                # get the images height for drawImage
                if start_sentence == "Puis":
                    img_height = add_image("assets/img/mountains.jpg", False)
                    images_height += img_height
                    
            #rest of the sentence
            end_sentence = story_part[end + 1:len(story_part)].strip()
                
            # has a custom word in the previous end_send that has a custom word
            for expression in ordered_custom_words:
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
        
    # add title
    height = two_fonts_title(width, title, proto_grotesk_regular, proto_grotesk_bold, spacing, "#000", top)
    font_effects_height += height
    
    # add end
    end_random = storydesign.StoryDesign.end_random
    img_end_height = add_image("assets/img/fin0"+ str(end_random) +".jpg", False)
    images_height += img_end_height
    
    # cut
    img_cut_height = add_image("assets/img/cut.jpg", False)
    images_height += img_cut_height

    height = top + before + title_margin_bottom + nb_lines * spacing + nb_parts * after_part + images_height + font_effects_height + bottom * 3
    return height
            


def two_fonts_title(width, title, regular_font, bold_font, spacing, text_color, top, context = False):
        
    effect_height = 0 
    height_spacing = 15
    title_parts = title.split(" ")
    effect_top = top
    left = 10
    line_words = []
    last_word = ""
    
    text_proto_regular = ImageFont.truetype(regular_font, 20, encoding="unic")
    text_proto_bold = ImageFont.truetype(bold_font, 48, encoding="unic")
    
    i = 0
    while i < len(title_parts):
        
        title_parts[i] = title_parts[i].upper()
        
        if i % 2 == 0:
            word_width, word_height = text_proto_regular.getsize(title_parts[i])
        else:
            word_width, word_height = text_proto_bold.getsize(title_parts[i])
    
        if left + word_width < width:
            line_words.append(title_parts[i]) # stock words in a line
            left += word_width + 10

        else:
            center_title(width, line_words, text_proto_regular, text_proto_bold, top, text_color, context)
            
            line_words = []
            line_words.append(title_parts[i]) # add cut word in the next line
            
            left = 10
            # add cut word width
            if i % 2 == 0:
                word_width, word_height = text_proto_regular.getsize(title_parts[i])
                left += word_width + 10 
            else :
                word_width, word_height = text_proto_bold.getsize(title_parts[i])
                left += word_width + 10 
            
            top += spacing + 20
            effect_height += spacing + 10
        
        # last line : draw
        if i == len(title_parts) -1 :
            center_title(width, line_words, text_proto_regular, text_proto_bold, top, text_color, context)
              
        i += 1
    
    effect_height += 60
    return effect_height


def center_title(width, line_words, text_proto_regular, text_proto_bold, top, text_color, context):
    
    line_left = 0
    for index, word in enumerate(line_words):
        if index % 2 == 0:
            word_width, word_height = text_proto_regular.getsize(word)
            line_left += word_width + 15 
        else :
            word_width, word_height = text_proto_bold.getsize(word)
            line_left += word_width + 15 
            
    center_left = (width - line_left) / 2
    for index, word in enumerate(line_words):
        if index % 2 == 0:
            word_width, word_height = text_proto_regular.getsize(word)
            if context : context.text((center_left, top), word, fill=text_color, font=text_proto_regular) # draw text
            center_left += word_width + 15 
        else :
            word_width, word_height = text_proto_bold.getsize(word)
            if context : context.text((center_left, top), word, fill=text_color, font=text_proto_bold) # draw text
            center_left += word_width + 15
    

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
    
    if start_sentence == "Il était une fois":
        words = start_sentence.split(" ", 2)
        part_one = (words[0] + ' ' + words[1]).upper() #manage latin caracter "é"
    elif start_sentence == "Il y a bien longtemps":
        words = ["Il y a", "bien lontemps"]
        part_one = words[0].upper()
    part_one_width, part_one_height = first_text_font.getsize(part_one)
    first_center_left = (width - part_one_width) / 2
    if context : context.text((first_center_left,effect_top), part_one, fill=text_color, font=first_text_font)
    effect_top += spacing
    height += spacing
    
    if start_sentence == "Il était une fois":
        part_two = words[2].upper()
    elif start_sentence == "Il y a bien longtemps":
        part_two = words[1].upper()
    part_two_width, part_two_height = second_text_font.getsize(part_two)
    second_center_left = (width - part_two_width) / 2
    if context : context.text((second_center_left,effect_top), part_two, fill=text_color, font=second_text_font)
    
    # add comma
    comma_left = second_center_left + part_two_width
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
    if context : context.text((comma_left, effect_top - 2), ', ', fill=text_color, font=text_maison_neue_book)
            
    return height


def space_between(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    effect_top = top + 5
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
    
    effect_top = top + 10
    text_first_font = ImageFont.truetype(first_font, first_font_size, encoding="unic")
    text_second_font = ImageFont.truetype(second_fond, second_font_size, encoding="unic")
                        
    words = start_sentence.split(" ")
    if len(words) == 2:
        # first word
        first_word_width, first_word_height = text_first_font.getsize(words[0] + ' ') # get text width
        if context : context.text((0, effect_top), words[0], fill=text_color, font=text_first_font) # draw text
                            
        # second word
        second_word_width, second_word_height = text_second_font.getsize(words[1]) # get text width
        if context : context.text((first_word_width, effect_top - 20), words[1], fill=text_color, font=text_second_font) # draw text
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
    rest_lines = textwrap.wrap(rest_part, width=27)
    for rest_line in rest_lines:
        context.text((0, effect_top), rest_line, fill=text_color, font=text_font)
        effect_top += spacing
    
    return effect_top


def vertical_syllable_mirror(width, start_sentence, font, font_size, spacing, text_color, top, context):
    
    top_offset = spacing / 2
    top += spacing - 15
    left = 0
    height = 0

    if start_sentence == "Heureusement":
        syllables = ["Heu", "reu", "se", "ment"]
        
                        
    # find the font size
    #target_font_size = get_font_size_syllables(width, syllables, font, font_size)
                                   
    # draw the text
    for index, syllable in enumerate(syllables):
            
        text_font = ImageFont.truetype(font, font_size - 2, encoding="unic")
        word = syllable.upper()
        syllable_width, syllable_height = text_font.getsize(word)
        if index % 2 == 0:
            context.text((left, top), word, fill=text_color, font=text_font)
        else:
            context.text((left, top - top_offset), word, fill=text_color, font=text_font)
                            
        left += syllable_width
        
        # add comma
        if index + 1 == len(syllables):
            text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
            if context : context.text((left, top - 2), ', ', fill=text_color, font=text_maison_neue_book)
    
        height = syllable_height - spacing
        
    return height

def decrease_syllale(width, start_sentence, font, font_size, spacing, text_color, top, context = False):
    
    effect_top = top
    left = 0
    height = 0

    if start_sentence == "Malheureusement":
        syllables = ["Mal", "heu", "reu", "se", "ment"]
        
    # find the font size
    #target_font_size = get_font_size_syllables(width, syllables, font, font_size)
                                   
    # draw the text
    for index, syllable in enumerate(syllables):
            
        text_font = ImageFont.truetype(font, font_size - 2, encoding="unic")
        word = syllable.upper()
        syllable_width, syllable_height = text_font.getsize(word)
        if context: context.text((left, effect_top), word, fill=text_color, font=text_font)
        
        effect_top += spacing / 4          
        left += syllable_width
        
        # add comma
        if index + 1 == len(syllables):
            text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
            if context : context.text((left, effect_top - 4), ', ', fill=text_color, font=text_maison_neue_book)
        
    return height


def increase_decrease(width, start_sentence, font, font_size, spacing, text_color, top, part_number, left = 0, context = False):

    effect_top = top
    height = 0
    result = []
    center_left_one = center_left_two = left
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    
    font_diff = 4
    font_size_one = font_size + 5

    if start_sentence == "De temps en temps":
        parts = ["De temps", "en temps"]
        
        for index, part in enumerate(parts):
            words = part.upper().split(" ")
            
            if index % 2 == 0:
                if part_number == 1:
                    results = manage_increase_decrease(part_number, words, font, font_size, text_font, spacing, text_color, effect_top, left, context)
                    center_left_one = results[0]
            else:
                if part_number == 2:
                    results = manage_increase_decrease(part_number, words, font, font_size, text_font, spacing, text_color, effect_top, left, context)
                    center_left_two = results[0]
                    word_height = results[1]
                    height += word_height + spacing
    
    result.extend([center_left_one, center_left_two, height])
    return result

def manage_increase_decrease(part_number, words, font, font_size, text_font, spacing, text_color, effect_top, left, context):
    
    font_diff = 4
    font_size_one = font_size + 5
    result = []
    
    word_width, word_height = text_font.getsize(words[0] + ' ')
    if part_number == 2: effect_top += word_height + spacing # text just below the effect first part 
    if context: context.text((left, effect_top), words[0], fill=text_color, font=text_font)
    left += word_width
                    
    letters = list(words[1])
    for letter in letters:
        if part_number == 1: text_font = ImageFont.truetype(font, font_size_one, encoding="unic")
        elif part_number == 2 : text_font = ImageFont.truetype(font, font_size_one + font_diff * len(words[1]), encoding="unic")
        letter_width, letter_height = text_font.getsize(letter) # redo after uppercase center text
        if left != 0 and context:
            if part_number == 1: context.text((left, effect_top), letter, fill=text_color, font=text_font)
            elif part_number == 2: context.text((left, effect_top - font_diff * len(words[1]) + 1), letter, fill=text_color, font=text_font)
        left += letter_width
        font_size_one += font_diff
        effect_top -= font_diff
    result.extend([left, word_height])
    return result

    
#get the font size of syllables to fulfil the paper width
def get_font_size_syllables(width, syllables, font, font_size):
    left = 0
    target_font_size = font_size
    
    while left <= width:
                            
        for index, syllable in enumerate(syllables):
            text_font = ImageFont.truetype(font, target_font_size, encoding="unic")
            word = syllable.upper()
            syllable_width, syllable_height = text_font.getsize(word)
                
            left += syllable_width
        target_font_size += 1
                            
        if left <= width: # init until condition is fulfil
            left = 0
            
    return target_font_size


def since(width, expression, font, font_size, spacing, text_color, top, context = False):
    effect_top = top
    height = 0
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    
    if expression == "Depuis ce jour":
        words = expression.split(" ", 1)
        first_part = words[0].upper()
        second_part = words[1].upper()
        
        first_part_width, first_part_height = text_font.getsize(first_part)
        if context : context.text((0, effect_top), first_part , fill=text_color, font=text_font)
        effect_top += spacing
        
        left = 2 * first_part_width / 3
        second_part_width, second_part_height = text_font.getsize(first_part)
        if context : context.text((left, effect_top), second_part , fill=text_color, font=text_font)
        
        # add comma
        text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
        comma_left = left + second_part_width + 15
        if context : context.text((comma_left, effect_top - 2), ', ', fill=text_color, font=text_maison_neue_book)
        
        height = 2 * spacing
    return height
    
    
def random_height(width, expression, font, font_size, spacing, text_color, top, context = False):
    effect_top = top + 10
    height = 0
    left = 0
    text_font = ImageFont.truetype(font, font_size, encoding="unic")
    
    
    letters = list(expression)
    for index, letter in enumerate(letters):
        letter = letter.upper()
        effect_top += randint(-5, 5)
        letter_width, letter_height = text_font.getsize(letter)
        if context : context.text((left, effect_top), letter , fill=text_color, font=text_font)
        left += letter_width
        
        # add comma
        if index + 1 == len(letters):
            text_maison_neue_book = ImageFont.truetype(maison_neue_book, 28, encoding="unic")
            comma_left = left
            if context : context.text((comma_left, effect_top - 2), ', ', fill=text_color, font=text_maison_neue_book)
        
        height = spacing
    return height


def get_left_place(width, expression, story_part, top, font_size, spacing):
    
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, font_size, encoding="unic")
    words = expression.split(" ")
    
    # cut sentence and delete first sentence
    rest_paragraph = story_part.split(". ", 1)
                    
    # get last part width
    rest_lines = textwrap.wrap(rest_paragraph[1], width=28)
    array_length = len(rest_lines)
    second_to_last = rest_lines[array_length - 2]
    last = rest_lines[array_length - 1]
    left = 0
    result = []
    
    
    if words[0] == "à": # particular case for 'à l'orée d'une forêt'
        first_word_second_last = re.search(r""+words[0]+r"\s", second_to_last)
        
        if first_word_second_last == None and re.search(r""+words[0]+r"\s", last) == None: # if word not in last part and not found in first
            left = 0
            top += spacing
    else :
        first_word_second_last = re.search(r"\b"+words[0]+r"\b", second_to_last)
    second_word_second_last = re.search(r"\b"+words[1]+r"\b", second_to_last)
    
    if words[0] == "à": # particular case for 'à l'orée d'une forêt'
        first_word_last = re.search(r""+words[0]+r"\s", last)
    else :
        first_word_last = re.search(r"\b"+words[0]+r"\b", last)
    second_word_last = re.search(r"\b"+words[1]+r"\b", last)

    
    # start to look in the second last part
    if first_word_second_last:
        first_position = first_word_second_last.start() # get position with space before : +1 delete space
        
        #find second word in the same part
        if second_word_second_last and second_word_second_last.start() > first_position:
            del_part = second_to_last[0:first_position]
            del_part_width, del_part_height = text_maison_neue_book.getsize(del_part)
            left = del_part_width + 2
        
        #find second word in the last part
        elif second_word_last:
            first_position = first_word_second_last.start()
            del_part = second_to_last[0:first_position] # from left paper to the cut word before expression
            del_part_width, del_part_height = text_maison_neue_book.getsize(del_part)
                        
            first_word_width, second_word_height = text_maison_neue_book.getsize(words[0])
            if del_part_width + first_word_width < width:
                left = del_part_width + 2
            else :
                left = 0
                top += spacing
                
    # look in the first last part
    elif first_word_last:
        first_position = first_word_last.start()
        if first_position == 0 :
            top += spacing
            left -= 4
        if second_word_last and second_word_last.start() > first_position:
            del_part = last[0:first_position]
            del_part_width, del_part_height = text_maison_neue_book.getsize(del_part)
            left = del_part_width + 2
        
                
    result.extend([left, top])
    return result


def place_img_position(width, expression, spacing, font_size, text_color, top, left, context, img):
    
    if expression == "au coeur de la jungle.":
        img_asset = "assets/img/jungle.jpg"
    elif expression == "à l'orée d'une forêt.":
        img_asset = "assets/img/forêt.jpg"
    elif expression == "près d'une cascade.":
        img_asset = "assets/img/cascade.jpg"
    elif expression == "sur la lune.":
        img_asset = "assets/img/lune.jpg"
    elif expression == "dans un coquillage.":
        img_asset = "assets/img/coquillage.jpg"
    
    # place in the sentence
    text_maison_neue_book = ImageFont.truetype(maison_neue_book, font_size, encoding="unic")
    words = expression.split(" ")
    for index, word in enumerate(words):
        if index == len(words) - 1: # if the last word correspond
            place_img = Image.open(img_asset)
            img_width, img_height = place_img.size
                            
            if (left + img_width > width): #if back to line
                comma_left = img_width
                if word != "cascade.":
                    add_image(img_asset, True, top, img)
                    context.text((comma_left, top), '.', fill=text_color, font=text_maison_neue_book)
                else:
                   add_image(img_asset, True, top + 5, img) 
            else:
                comma_left = left + img_width
                if word != "cascade.":
                    add_image(img_asset, True, top - spacing, img, left)
                    context.text((comma_left, top - spacing), '.', fill=text_color, font=text_maison_neue_book)
                else:
                    add_image(img_asset, True, top - spacing + 6, img, left)
        else :    
            context.text((left,top - spacing), word, fill=text_color, font=text_maison_neue_book)
            word_width, word_height = text_maison_neue_book.getsize(word)
            left += word_width + 5
            if (left + word_width) > width:
                left = 0
                top += spacing

    
def imposed_event(width, expression, contour_word, top, font_bold, font_contour, font_size, after_part, spacing, text_color, context = False):
    
    text_event_bold = ImageFont.truetype(font_bold, font_size + 12, encoding="unic")
    text_event_contour = ImageFont.truetype(font_contour, font_size + 5, encoding="unic")
		    
    words = expression.split(" ")
    top += after_part
    left = 0
    effect_height = after_part
		    
    for word in words:
        if word == 'météorites':
            contour_word = u'météorites'.upper()
        elif word == 'guerrière':
            contour_word = u'guerrière'.upper()
        
        word = word.upper()
        word_width, word_height = text_event_bold.getsize(word)
                        
        if left + word_width < width:
        
            if word == contour_word.upper():
                if context : context.text((left, top + 4), word, fill=text_color, font=text_event_contour) # draw text
            else:
                if context : context.text((left, top), word, fill=text_color, font=text_event_bold) # draw text
            left += word_width + 10
        else:
            top += spacing + 10
            effect_height += spacing + 10
            left = 0
            if word == contour_word.upper():
                if context : context.text((left, top + 4), word, fill=text_color, font=text_event_contour) # draw text
            else:
                if context : context.text((left, top), word, fill=text_color, font=text_event_bold) # draw text
            left += word_width + 10
 
    if contour_word == "sorcier" or contour_word == "tornade":
        if context : context.text((left - 10, top), '.', fill=text_color, font=text_event_bold) # draw text
    
    return effect_height

def add_image(url, add, top = 0, img_bg = False, left = 0):
    custom_img = Image.open(url)
    if add == True : img_bg.paste(custom_img, (left, top))
    img_width, img_height = custom_img.size
        
    return img_height
