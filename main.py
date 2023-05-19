from os.path import isfile

import requests
import telebot

from telebot import types

token = open("token.txt").readline()
bot = telebot.TeleBot(token)

global_user_ready_to_signin = False
global_user_ready_to_recognition=False


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Menu', reply_markup=make_button())


def send_menu(message):
    bot.edit_message_text(chat_id= message.chat.id,message_id=message.id, text= 'Menu', reply_markup=make_button())


# this method send description and create button "back"
def send_description(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    bot.send_message(message.chat.id, "Developers of this bot Salavat & Nikita")
    buttonA = types.InlineKeyboardButton("back", callback_data="back")
    markup.add(buttonA)
    bot.edit_message_text(chat_id = message.chat.id,message_id=message.id, text='You choose description',reply_markup=markup)

# this method give answer on user request thought button
@bot.callback_query_handler(func =lambda call:True)
def callback(call):
    if call.message:
        if call.data == "description":
            send_description(call.message)
        if call.data == "sign in":
            global global_user_ready_to_signin
            global_user_ready_to_signin=True
            bot.send_message(call.message.chat.id, "Send your voice")
        if call.data == "recognition":
            global global_user_ready_to_recognition
            global_user_ready_to_recognition = True
            bot.send_message(call.message.chat.id, "send voice message, please")
        if call.data == "back":
            send_menu(call.message)


# This method give answer if user send voice message.
# In body of method checked that user create request from button
@bot.message_handler(content_types=['voice'])
def download_voice_message(message):
    global global_user_ready_to_signin
    global global_user_ready_to_recognition
    if (global_user_ready_to_signin):
        global_user_ready_to_signin=False
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(f'user_voice_from_chat_{message.chat.id}.ogg', 'wb') as f:
            f.write(file.content)
            f.close()
        bot.send_message(message.chat.id,"We got your voice")
    if (global_user_ready_to_recognition):
        global_user_ready_to_recognition=False
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(f'user_voice_from_chat_{message.chat.id}_for_recognition.ogg', 'wb') as f:
            f.write(file.content)
            f.close()
        pathToAudioFile_usedDuringRegistration = f'user_voice_from_chat_{message.chat.id}.ogg'
        pathToAudioFile_usedForRecognition = f'user_voice_from_chat_{message.chat.id}_for_recognition.ogg'
        if(isfile(pathToAudioFile_usedDuringRegistration)):
            bot.send_message(message.chat.id, "We got your voice message, please waiting...")
            #запускаем скрипт распознования голоса
            pass
        else:
            bot.send_message(message.chat.id,"Your account is not registered")
    else:
        bot.send_message(message.chat.id,"Please, choose action")
    start_message(message)


def make_button():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttonA = types.InlineKeyboardButton("description", callback_data="description")
    buttonB = types.InlineKeyboardButton("sign in", callback_data="sign in")
    buttonC = types.InlineKeyboardButton("recognition", callback_data="recognition")
    markup.add(buttonA, buttonB, buttonC)
    return markup

bot.infinity_polling()



