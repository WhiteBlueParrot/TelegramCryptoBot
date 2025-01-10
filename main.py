import telebot

from config import TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = 'Привет! Я бот, который умеет конвертировать валюту!\n\n' \
           'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key, ))  # Without the comma,
        # Python would interpret (text, key) as a simple grouping of values, rather than a tuple.
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров!')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров!')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.reply_to(message, text)


bot.polling(non_stop=True)
