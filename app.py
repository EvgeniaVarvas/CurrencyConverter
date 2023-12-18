import telebot
from telebot import types
from config import TOKEN
from keys import keys
from extensions import СurrencyСonverter, ConversionException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def start(message: types.Message):

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_help = types.InlineKeyboardButton(text='Помощь', callback_data='help')
    btn_values = types.InlineKeyboardButton(text='Валюта', callback_data='values')
    
    markup.add(btn_help, btn_values)
    bot.send_message(message.chat.id, text="Конвертер валют.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'values':
        values(call.message)
    elif call.data == 'help':
        help(call.message)


@bot.message_handler(commands=['start',])
def help(message: types.Message):
    text = "Чтобы начать работу введите команду в следующем формате:\n<название валюты>\n<в какую валюту перевести>\n\
<количество переводимой валюты>"
    bot.send_message(message.chat.id, text=text)
@bot.message_handler(commands=['values'])    
def values(message: types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: types.Message):
    try:
        values = message.text.split(' ')
        if len(values)!=3:
            raise ConversionException('Неверное количество параметров.')
        
        quote, base, amount = values
        total_base = СurrencyСonverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')    
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{message.text}') 
    else:
        bot.send_message(message.chat.id, f'{amount} {quote} = {float(amount)*float(total_base)} {base}')       
bot.polling()