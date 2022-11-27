import telebot
from config import keys, TOKEN
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Введите через пробел:" \
           "\n<Название валюты для покупки>\n<Название валюты оплаты>\n<Сколько нужно купить в виде 0.00>\n " \
           "Чтобы просмотреть доступные валюты, нажмите тут: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def  get_price(message: telebot.types.Message):
    values = message.text.split(' ')
    base, quote, qty = values
    try:
        if len(values) != 3:
            raise APIException("(Пожалуйста, введите три параметра через пробел")
        elif quote == base:
            raise APIException("Названия валют не должны совпадать")
        total_base = Converter.get_price(base, quote, qty)
    except APIException as er:
        bot.send_message(message.chat.id, f'Ошибка пользователя: {er}')
    except BaseException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    else:
        text = f'Итого: {qty} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()