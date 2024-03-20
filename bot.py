import telebot
from telebot import formatting
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import upcoming_content

def escape_special_characters(input_text):
    special_characters = ['_', '[', ']', '(', ')', '~', '`', '>',
                          '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_characters:
        input_text = input_text.replace(char, f'\\{char}')
    return input_text

##TELEGRAM STUFF
API_KEY = '7144244211:AAHKIOSCx7A6RYiJv2t6RuYevT_Vp1nk2DA'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):

    # KEYBOARD MARKUP/BUTTONS SECTION
    markup_reply = ReplyKeyboardMarkup(resize_keyboard=True)
    films = KeyboardButton(text='Films')
    tv = KeyboardButton(text='TV Shows')
    games = KeyboardButton(text='Games')

    row1 = [films]
    row2 = [tv]
    row3 = [games]

    markup_reply.add(*row1)
    markup_reply.add(*row2)
    markup_reply.add(*row3)

    msg = bot.send_message(message.chat.id,
                           "Click the buttons!",
                           reply_markup=markup_reply
                           )

def main_process(message,results):

    bot.send_message(message.chat.id, "Loading results, please wait...")

    if results == []:
        bot.send_message(message.chat.id, 'An error occurred. Please contact: https://t.me/tImoHyDe')
    else:

        for result in results:

            name = result[0]
            image = result[1]
            description = result[2]
            trailer_name = name.replace(' ', '') + 'trailer'
            trailer_link = f'https://www.google.com/search?q={trailer_name}&tbm=vid'

            bold_part_name = formatting.mbold("Name")
            regular_part_name = f"{name}"
            mixed_text_name = bold_part_name + ": " + regular_part_name

            bold_part_image = formatting.mbold("Image")
            regular_part_image = f"{image}"
            mixed_text_image = bold_part_image + ": " + regular_part_image

            bold_part_description = formatting.mbold("Description")
            regular_part_description = f"{description}"
            mixed_text_description = bold_part_description + ": " + regular_part_description

            bold_part_trailer_link = formatting.mbold("Trailer Link")
            regular_part_trailer_link = f"{trailer_link}"
            mixed_text_trailer_link = bold_part_trailer_link + ": " + regular_part_trailer_link

            bot.send_message(message.chat.id,
f'''
{escape_special_characters(mixed_text_name)}

{escape_special_characters(mixed_text_image)}

{escape_special_characters(mixed_text_description)}

{escape_special_characters(mixed_text_trailer_link)}

''',parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def handle_start_response(message):

    if message.text == 'TV Shows':

        results = upcoming_content.imdb_top_content(num_results=5,content_type='tv_series')

        main_process(message,results)

    elif message.text == 'Games':

        bot.send_message(message.chat.id, "Loading results, please wait...")

        results = upcoming_content.imdb_top_content(num_results=5, content_type='video_game')

        main_process(message, results)

    else:

        bot.send_message(message.chat.id, "Loading results, please wait...")

        results = upcoming_content.imdb_top_content(num_results=5, content_type='feature')

        main_process(message,results)

bot.polling()