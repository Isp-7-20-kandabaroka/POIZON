import telebot
from telebot import types

bot_token = '6385392149:AAH2tONppORrG8GjFRFu5MpoREpx0TjmFEs'
bot = telebot.TeleBot(bot_token)
exchange_rate = 14.7
DELIVERY_COST = 1500
calculator_mode = {}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['start'])
def start_message(message):
    show_main_keyboard(message)

@bot.message_handler(content_types=['text'], func=lambda msg: not msg.text.startswith('/'))
def handle_text_message(message):
    faq_text = """FAQ 📚
    • Оформление заказа:
    — Заказы принимаются только через Telegram
    @skbdkclth

    • Оплата и доставка:
    — Вы можете совершить оплату переводом на карту Тинькофф
    — Для доставки вам необходимо предоставить следующие данные:
    - ФИО
    - Номер телефона
    - Эл. почта
    - Почтовый индекс
    — Стоимость доставки Китай - Москва 1500р
    — Стоимость доставки по России 300-500р
    — Отправка любой транспортной компанией

    • Сколько времени занимает доставка?
    — По Китаю 2-3 дня с момента выкупа
    — Китай - Москва 3-4 недели (Быстрая доставка 2-3 дня до Москвы 30$/кг)
    — По России 3-5 дней с момента отправки.
    Все зависит от удаленности вашего города.
    Примечание*
    — Магазин не берет своих комиссий
    Как узнать цену ⬇️

    
    """



    if message.text == 'FAQ 📚':
        calculator_mode[message.chat.id] = False

        photo1 = open('price/photo_2023-10-14_22-57-45.jpg', 'rb')
        photo2 = open('price/photo_2023-10-14_22-57-46.jpg', 'rb')
        # Создаем объект сообщения с типом "photo" для каждой фотографии
        photo1_message = telebot.types.InputMediaPhoto(photo1)
        photo2_message = telebot.types.InputMediaPhoto(photo2)
        txt = '«Именно эту цену вы пишите в калькулятор цен💱»'
        # Объединяем объекты сообщений в одном массиве
        photos = [photo1_message, photo2_message]


        # Отправляем сообщение с фотографиями

        bot.send_message(message.chat.id ,faq_text)
        bot.send_media_group(message.chat.id, photos)
        send_and_show_back_button(message,txt)

    elif message.text == 'ОФОРМИТЬ ЗАКАЗ 📝':
        calculator_mode[message.chat.id] = False
        send_and_show_back_button(message, 'Чтобы оформить заказ обращайтесь:\n 🛒@skbdkclth🛒')
    elif message.text == 'КАЛЬКУЛЯТОР ЦЕН 💱':
        calculator_mode[message.chat.id] = True
        photo_path = 'price/photo_2023-10-14_11-38-23.jpg'
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file, caption='💰 Введите цену товара в юанях.')
        show_back_keyboard(message)
    elif is_number(message.text) and calculator_mode.get(message.chat.id, False):
        process_number(message)
        show_back_keyboard(message)
    elif message.text == 'НАЗАД ⬅️':
        calculator_mode[message.chat.id] = False
        show_main_keyboard(message)
    else:
        bot.send_message(message.chat.id, '😔 Я вас не понимаю. Пожалуйста, выберите одну из опций.')
        show_back_keyboard(message)


def show_main_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row("FAQ 📚", "ОФОРМИТЬ ЗАКАЗ 📝", "КАЛЬКУЛЯТОР ЦЕН 💱")
    bot.send_message(message.chat.id, 'Добро пожаловать! Выберите что хотите сделать', reply_markup=keyboard)

def show_back_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("НАЗАД ⬅️")
    bot.send_message(message.chat.id, '_', reply_markup=keyboard)

def send_and_show_back_button(message, text):
    bot.send_message(message.chat.id, text)
    show_back_keyboard(message)

def process_number(message):
    yuan_price = float(message.text)
    ruble_price = yuan_price * exchange_rate
    total_price = ruble_price + DELIVERY_COST
    bot.reply_to(message,
                 f'Цена товара в рублях: {ruble_price} 🛒\n(расчет: {yuan_price} юаней * {exchange_rate} руб./юань)'
                 f'\n\nЦена товара с учетом доставки: {total_price} 📦\n(расчет: {ruble_price} руб. + {DELIVERY_COST} руб. доставка)'
                 f'Готов оформить заказ? Тогда пиши @skbdkclth сюда.')

admin_id = '940423408'  # замените на свой Telegram ID

@bot.message_handler(content_types=['text'], commands=['set_rate'], func=lambda msg: msg.text.startswith('/'))
def handle_set_rate_command(message):
    if str(message.chat.id) != admin_id:
        bot.send_message(message.chat.id, 'У вас нет прав для выполнения этой команды.')
        return

    # Проверяем, правильно ли составлено сообщение
    # Сообщение должно быть: /set_rate 15.7, где 15.7 - новый курс
    args = message.text.split()
    if len(args) != 2 or not is_number(args[1]):
        bot.send_message(message.chat.id, 'Неправильный формат команды. Пример: /set_rate 14.7')
        return

    # Меняем курс обмена
    global exchange_rate
    exchange_rate = float(args[1])
    bot.send_message(message.chat.id, f'Новый курс обмена установлен: {exchange_rate}')
bot.infinity_polling()