import telebot
from telebot import types


class MenuButtonBuilder:
    @staticmethod
    def make_button():
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttonA = types.InlineKeyboardButton("description", callback_data="description")
        buttonB = types.InlineKeyboardButton("sign in", callback_data="sign in")
        markup.add(buttonA, buttonB)
        return markup