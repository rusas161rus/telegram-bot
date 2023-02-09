import config
import datetime
import telebot
import logging
from telebot import types

logger=telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot=telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['s'])
def button(message):        
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btm1=types.KeyboardButton('Инструкция ⚙️')
    btm2=types.KeyboardButton('Заявка 🛠')
    btm3=types.KeyboardButton('Контакты 📱')
    btm4=types.KeyboardButton('Мой-ID 🪪')
    btm5=types.KeyboardButton('Файл 📎')        
    markup.add(btm1, btm4, btm3, btm2, btm5)
    bot.send_message(message.chat.id, 'Бот запущен!', reply_markup=markup)

@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video', 'voice']) 

def send_text(message):
    if message.text=='Мой-ID 🪪':
        bot.send_message(message.chat.id, "Ваш логин: {0.username} и Ваш ID: {0.id}.".format(message.from_user, bot.get_me(),
    parse_mode='html'))
    if message.text=='Контакты 📱':
        bot.send_message(message.chat.id, "Телефон тех поддержки: 863****064 доб. 137".format(message.from_user, bot.get_me(),
    parse_mode='html'))
    if message.text=='Инструкция ⚙️':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Инструкция_1 ⚙️", url="https://yandex.ru/search/?clid=2437996&text=z&l10n=ru&lr=39"))
        markup.add(types.InlineKeyboardButton("Инструкция_2 ⚙️", url="https://yandex.ru/search/?clid=2437996&text=z&l10n=ru&lr=39"))
        bot.send_message(message.chat.id, 'Нажмите кнопку!', reply_markup=markup)   

    if message.text=='Заявка 🛠':
        msg=bot.send_message(message.chat.id, "<b>Ваш логин: {0.username} и Ваш ID: {0.id}.</b>\n\n{0.first_name} {0.last_name}, здравствуйте! Меня зовут - {1.first_name}.\n\n<b>{0.first_name}</b> я зарегистрирую Вашу заявку, для этого в начале сообщения <u><b>введите Ваш ID</b></u> и подробно опишите, что случилось?".format(message.from_user, bot.get_me()),
        parse_mode='html')
        bot.register_next_step_handler(msg, create_request_0)
    
    if message.text=='Файл 📎':
        msg=bot.send_message(message.chat.id, "<b>Здравствуйте, Ваш ID: {0.id}.</b>\n\nОбращаю ваше внимание, что можно отправить только файл, без текста, в названии файла нужно указать <u><b>Ваш ID</b></u>".format(message.from_user, bot.get_me()),
        parse_mode='html')
        bot.register_next_step_handler(msg, create_request_1)
        
    # Повторный модуль, для коротких команд
    if message.text=='Мой-ID':
        bot.send_message(message.chat.id, "Ваш логин: {0.username} и Ваш ID: {0.id}.".format(message.from_user, bot.get_me(),
    parse_mode='html'))
    if message.text=='Контакты':
        bot.send_message(message.chat.id, "Телефон тех поддержки: 8633032064 доб. 137".format(message.from_user, bot.get_me(),
    parse_mode='html'))
    if message.text=='Инструкция':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Инструкция ⚙️", url="https://yandex.ru/search/?clid=2437996&text=z&l10n=ru&lr=39"))
        bot.send_message(message.chat.id, 'Нажмите кнопку!', reply_markup=markup)   

    if message.text=='Заявка':
        msg=bot.send_message(message.chat.id, "<b>Ваш логин: {0.username} и Ваш ID: {0.id}.</b>\n\n{0.first_name} {0.last_name}, здравствуйте! Меня зовут - {1.first_name}.\n\n<b>{0.first_name}</b> я зарегистрирую Вашу заявку, для этого в начале сообщения <u><b>введите Ваш ID</b></u> и подробно опишите, что случилось?".format(message.from_user, bot.get_me()),
        parse_mode='html')
        bot.register_next_step_handler(msg, create_request_0)
    
    if message.text=='Файл':
        msg=bot.send_message(message.chat.id, "<b>Здравствуйте, Ваш ID: {0.id}.</b>\n\nОбращаю ваше внимание, что можно отправить только файл, без текста, в названии файла нужно указать <u><b>Ваш ID</b></u>".format(message.from_user, bot.get_me()),
        parse_mode='html')
        bot.register_next_step_handler(msg, create_request_1)
    # Повторный модуль, для коротких команд

def create_request_0(message):
    data=[]
    today=datetime.datetime.today()
    data.append(today)              
    f=open("file.txt", "a")
    f.write("\n\n{Новая заявка}, {0.id}\n")
    f.write(today.strftime("%Y-%m-%d-%H.%M.%S"))
    f.write("|ID|")
    while True:
        try:
            f.write(message.text)
        except AttributeError:
            bot.send_message(message.chat.id, 'Попробуйте снова! Нажмите кнопку "Заявка"')
        except TypeError:
            bot.send_message(message.chat.id, 'Попробуйте снова! Нажмите кнопку "Заявка"')
        except UnicodeEncodeError:
            bot.send_message(message.chat.id, 'Попробуйте снова! Нажмите кнопку "Заявка"')
        else:            
            f.close()  
            bot.send_message(message.chat.id, 'Передал отвественным специалистам, дальнейшие сообщения переданы не будут. Если забыли, что то дописать, тогда нажмите кнопку "Заявка"'.format(name=message.text), parse_mode='html')
        finally:
            break
   
def create_request_1(message):
    while True:
        try:
            file_name=message.document.file_name
        except AttributeError:
            bot.send_message(message.chat.id, 'Попробуйте снова! Нажмите кнопку "Файл"')            
        else:
            file_name=message.document.file_name
            file_info=bot.get_file(message.document.file_id)
            downloaded_file=bot.download_file(file_info.file_path)
            with open('C:/Users/budnikovra/Desktop/test/1/' + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, 'Файл загружен'.format(name=message.text), parse_mode='html')
        finally:
            break      


bot.polling(none_stop=True, timeout=30)
    
