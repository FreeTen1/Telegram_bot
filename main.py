import telebot
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['values', ])
def cmd_values(message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text += key + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start', 'help', ])
def help_start(message):
    bot.send_message(message.chat.id, "Отправьте сообщение боту в виде <имя валюты> <имя "
                                      "валюты в которую надо перевести> <количество первой "
                                      "валюты>\nПример:\nдоллар рубль 5\nСписок всех доступных волют можно узнать "
                                      "введя команду /values")


@bot.message_handler(content_types=["text", ])
def conversion(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное кол-во параметров')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка!\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'не удалось обработать команду\n{e}')
    else:
        text = f"{amount} {quote} = {round(total_base, 4)} {base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
