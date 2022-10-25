import requests
import telebot
from config import keys, TOKEN
from Extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcom(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Велком, {message.chat.username}! \
    Для начала работы напиши или нажми /help")


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        f"{message.chat.username}, я могу посчитать для тебя стоимость некоторых "
        f"валют по сегодняшнему курсу))"
        f"\nДля этого напиши через пробел с маленькой буквы: "
        f"\n<имя валюты> \n<в какую перевести> \n<количество цифрой>."
        f"\nСписок доступных валют здесь: /values"
    )


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Много/мало параметров. Введи текст еще раз.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду "\n{e}"')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)