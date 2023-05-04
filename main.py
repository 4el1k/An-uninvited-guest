import requests
import telebot

from telebot import types

token = open("token.txt").readline()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Menu', reply_markup=make_button())


def send_menu(message):
    bot.edit_message_text(chat_id= message.chat.id,message_id=message.id, text= 'Menu', reply_markup=make_button())

def send_description(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    bot.send_message(message.chat.id, "Developers of this bot Salavat & Nikita")
    buttonA = types.InlineKeyboardButton("back", callback_data="back")
    markup.add(buttonA)
    bot.edit_message_text(chat_id = message.chat.id,message_id=message.id, text='You choose description',reply_markup=markup)


@bot.callback_query_handler(func =lambda call:True)
def callback(call):
    if call.message:
        if call.data == "description":
            send_description(call.message)
        if call.data == "sign in":
            global global_user_ready_to_signin
            global_user_ready_to_signin=True
            bot.send_message(call.message.chat.id, "Send your voice")
        if call.data == "back":
            send_menu(call.message)


@bot.message_handler(content_types=['voice'])
def download_voice_message(message):
    if (global_user_ready_to_signin):
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(f'user_voice_from_chat_{message.chat.id}.ogg', 'wb') as f:
            f.write(file.content)
            f.close()
        bot.send_message(message.chat.id,"We got your voice")
        start_message(message)

def make_button():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttonA = types.InlineKeyboardButton("description", callback_data="description")
    buttonB = types.InlineKeyboardButton("sign in", callback_data="sign in")
    markup.add(buttonA, buttonB)
    return markup

bot.infinity_polling()



