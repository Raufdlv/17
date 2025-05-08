from telebot import TeleBot
from buttons import *
from database import *

bot = TeleBot("7455699017:AAH0lohNU5Vu2xmsCNmCFbefn-K7Mj7ls2w")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Пожалуйста, выберите язык / Iltimos, tilni tanlang", reply_markup=language_menu())

@bot.message_handler(func=lambda message: message.text in ["Русский 🇷🇺", "O‘zbek 🇺🇿"])
def choose_language(message):
    user_id = message.from_user.id
    lang = 'ru' if message.text == "Русский 🇷🇺" else 'uz'
    set_user_lang(user_id, lang)
    bot.send_message(user_id, "Язык выбран!" if lang == 'ru' else "Til tanlandi!", reply_markup=main_menu(lang))

@bot.message_handler(func=lambda message: message.text in ["Ввести имя", "Ismni kiriting"])
def ask_name(message):
    lang = get_user_lang(message.from_user.id)
    bot.send_message(message.chat.id, "Введите ваше имя:" if lang == 'ru' else "Ismingizni kiriting:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    lang = get_user_lang(user_id)
    bot.send_message(user_id,
                     f"Отлично, {name}. Пожалуйста, отправьте свой номер" if lang == 'ru'
                     else f"Ajoyib, {name}. Iltimos, raqamingizni yuboring",
                     reply_markup=contact_button(lang))
    bot.register_next_step_handler(message, get_phone, name)

def get_phone(message, name):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)

    if message.contact:
        phone_number = message.contact.phone_number
        add_user(user_id, name, phone_number, lang)
        bot.send_message(user_id,
                         f"Вы успешно прошли регистрацию, {name}!\nВаш номер: {phone_number}" if lang == 'ru'
                         else f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz, {name}!\nRaqamingiz: {phone_number}",
                         reply_markup=main_menu(lang))
    else:
        bot.send_message(user_id,
                         "Отправьте свой номер через кнопку в меню." if lang == 'ru'
                         else "Raqamingizni menyudagi tugma orqali yuboring.",
                         reply_markup=contact_button(lang))
        bot.register_next_step_handler(message, get_phone, name)

@bot.message_handler(func=lambda message: message.text in ["Список пользователей", "Foydalanuvchilar ro'yxati"])
def show_users(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    users = get_all_users()

    if not users:
        bot.send_message(user_id, "Список пользователей пуст." if lang == 'ru' else "Foydalanuvchilar ro'yxati bo'sh.")
        return

    header = f"Всего пользователей: {len(users)}\n\n" if lang == 'ru' else f"Foydalanuvchilar soni: {len(users)}\n\n"
    text = header

    for user in users:
        uid, name, phone, _, _ = user
        text += f"ID: {uid}\nИмя: {name}\nНомер: {phone}\n\n" if lang == 'ru' else f"ID: {uid}\nIsmi: {name}\nRaqami: {phone}\n\n"

    bot.send_message(user_id, text)

bot.infinity_polling()
