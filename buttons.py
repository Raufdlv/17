from telebot.types import *

def language_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Русский 🇷🇺", "O‘zbek 🇺🇿")
    return markup

def main_menu(lang='ru'):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("Ввести имя"))
        markup.add(KeyboardButton("Список пользователей"))
    else:
        markup.add(KeyboardButton("Ismni kiriting"))
        markup.add(KeyboardButton("Foydalanuvchilar ro'yxati"))
    return markup

def contact_button(lang='ru'):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    text = "Отправить номер" if lang == 'ru' else "Raqamni yuborish"
    markup.add(KeyboardButton(text, request_contact=True))
    return markup
