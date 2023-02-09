import config
import sqlconnect
import psycopg2
from psycopg2 import Error
import telebot
import logging
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename = "log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot=telebot.TeleBot(config.TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name        

@bot.message_handler(commands = ['s'])
def button(message):      
    markup=types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 3)
    btm4=types.KeyboardButton('Мои-ID и Мои заявки ✅')
    btm7=types.KeyboardButton('Мой-ID 🪪')
    btm5=types.KeyboardButton('Контакты и Инструкции📱')        
    markup.add(btm4, btm7, btm5)
    btm6=types.KeyboardButton('Найти Заявку 🔍')        
    markup.add(btm6)       
    btm1=types.KeyboardButton('Создать Заявку 🛠')
    btm2=types.KeyboardButton('Дополнить Заявку 🛠')
    btm3=types.KeyboardButton('Удалить Заявку ⛔️') 
    markup.add(btm1, btm2, btm3)
    msg = bot.send_message(message.chat.id, 'Бот запущен!', reply_markup = markup)
    bot.register_next_step_handler(msg, next_step_handler)
 
@bot.message_handler(content_types = ['text', 'document', 'photo', 'audio', 'video', 'voice'])
def next_step_handler(message):     
    try:        
        chat_id = message.chat.id
        name = message.from_user.id
        user = User(name)
        user_dict[chat_id] = user
         
        if message.text == 'Контакты и Инструкции📱':
            bot.send_message(message.chat.id, "Телефон тех поддержки: 8633032064 доб. ххх".format(message.from_user, bot.get_me(),
        parse_mode='html'))
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Инструкция_1 ⚙️", url = "https://yandex.ru/search/?clid=2437996&text=z&l10n=ru&lr=39"))
            markup.add(types.InlineKeyboardButton("Инструкция_2 ⚙️", url = "https://yandex.ru/search/?clid=2437996&text=z&l10n=ru&lr=39"))
            bot.send_message(message.chat.id, 'Нажмите кнопку!', reply_markup = markup)             

        if message.text == 'Создать Заявку 🛠':
            msg=bot.send_message(message.chat.id, "{0.first_name} {0.last_name}, здравствуйте! Меня зовут - {1.first_name}.\n\n<b>{0.first_name}</b> я зарегистрирую Вашу заявку, для этого введите <u><b>Название заявки</b></u>!".format(message.from_user, bot.get_me()),
            parse_mode = 'html')        
            bot.register_next_step_handler(msg, create_request_0)        

        if message.text == 'Дополнить Заявку 🛠':
            msg=bot.send_message(message.chat.id, "{0.first_name} {0.last_name}, здравствуйте!\n\n Для обновления заявки введите её номер".format(message.from_user, bot.get_me()),
            parse_mode = 'html')            
            bot.register_next_step_handler(msg, create_request_1)
    
        if message.text == 'Удалить Заявку ⛔️':
            msg=bot.send_message(message.chat.id, "{0.first_name} {0.last_name}, здравствуйте!  Для удаления заявки напишите её номер, <b>Обратите внимание, это действие не обратимо!</b>".format(message.from_user, bot.get_me()),
            parse_mode = 'html')        
            bot.register_next_step_handler(msg, create_request_3)

        if message.text == 'Мой-ID 🪪':                       
            bot.send_message(message.chat.id, "Ваш логин: {0.username} и Ваш ID: {0.id}.".format(message.from_user, bot.get_me(),
            parse_mode='html'))        
        print(message.from_user.last_name)
        if message.text == 'Мои-ID и Мои заявки ✅':                       
            bot.send_message(message.chat.id, "Ваш логин: {0.username} и Ваш ID: {0.id}.".format(message.from_user, bot.get_me(),
            parse_mode='html'))   

        if message.text == 'Найти Заявку 🔍':
            msg=bot.send_message(message.chat.id, "{0.first_name} {0.last_name}, здравствуйте! Напишите номер заявки".format(message.from_user, bot.get_me()),
            parse_mode = 'html')        
            bot.register_next_step_handler(msg, create_request_4)     
            


        if message.text == 'Мои-ID и Мои заявки ✅':
            try: 
                connection = psycopg2.connect(  user = sqlconnect.USER, 
                                                password = sqlconnect.PASSWORD, 
                                                host = sqlconnect.HOST, 
                                                port = sqlconnect.PORT, 
                                                database = sqlconnect.DATABASE)
                id_us = [message.from_user.id]
                cursor = connection.cursor()                              
                cursor.execute("SELECT * from CRM_TABLE where USER_ID = %s".format(message.text), (id_us))
                connection.commit()            
                record = cursor.fetchall()
                for row in record:
                    a = str(row[0])
                    #b = str(row[10])
                    #c = str(row[11])
                    d = str(row[12])
                    #e = str(row[13])
                    f = str(row[8])
                    g = str(row[1])
                    raspis=(" | №=" + a + " | Дата и время обращения \n" + f  + "\n\n  | Название заявки =" + g + "\n  | Статус заявки =" + d)
                    bot.send_message(message.chat.id, raspis)
            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
                bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
            finally:                        
                if connection:                           
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")

    except Exception as e:
        bot.reply_to(message, 'oooops')

def create_request_0(message):
    global text_2
    text_2 = message.text
    msg=bot.send_message(message.chat.id, "Напишите, что случилось.".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_5)        

def create_request_1(message):
    global text_1
    text_1 = [message.text]
    msg=bot.send_message(message.chat.id, "Напишите текст заявки".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_2)
   


def create_request_5(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        id_h=[text_2, message.chat.id, message.id, message.from_user.id, str(message.from_user.username), str(message.from_user.last_name), str(message.from_user.first_name)]
        cursor = connection.cursor()                              
        cursor.execute("""INSERT INTO CRM_TABLE (NAZVANIE_ZAIVKI, CHAT_ID, MESSAGE_ID, USER_ID, USER_NAME, USER_LAST_NAME, USER_FERST_NAME, TEXT_ZAIVKI, STATUS_ZAIVKI) 
                                          VALUES (%s, %s, %s, %s, %s, %s, %s, '{}', 'Зарегистрировано')""".format(message.text), (id_h))
        cursor.execute("SELECT * from CRM_TABLE".format(message.text))
        connection.commit()
        record = cursor.fetchall()
        for row in record:
            a = str(row[0])
        raspis=("Зявка успешно зарегистрирована, номер вашей заявки: " + a)
        bot.send_message(message.chat.id, raspis) 
        print(cursor.rowcount, "1 Запись успешно Вставлена") 
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при Регистрации заявки".format(name = message.text))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_request_2(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)        
        cursor = connection.cursor()              
        cursor.execute("""Update CRM_TABLE set TEXT_DOP_ZAIVKI = ('{}') WHERE ID = %s""".format(message.text), (text_1))
        connection.commit()
        print(cursor.rowcount, "Запись успешно обновлена")        
        bot.send_message(message.chat.id, "Запись успешно обновлена".format(name = message.text))   
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:                        
        if connection:                           
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_request_3(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)            
        cursor = connection.cursor()                              
        cursor.execute("""Delete from CRM_TABLE where id = ('{}')""".format(message.text))
        connection.commit()
        print(cursor.rowcount, "Запись успешно удалена")        
        bot.send_message(message.chat.id, "Запись успешно удалена".format(name = message.text))  
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_request_4(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)            
        cursor = connection.cursor()                              
        cursor.execute("SELECT * from CRM_TABLE where ID = ('{}')".format(message.text))
        connection.commit()
        record = cursor.fetchall()
        for row in record:
            a = str(row[0])
            b = str(row[10])
            c = str(row[11])
            d = str(row[12])
            e = str(row[13])
            f = str(row[8])
            g = str(row[1])
            raspis=(" | №=" + a + " | Дата и время обращения \n" + f  + ",\n\n  | Название заявки =" + g + "\n\n  | Статус заявки =" + d +  "\n | Решение специалиста =" + e + "\n\n | Описание =" + b + "\n\n | Дополненое описание =" + c)
            bot.send_message(message.chat.id, raspis)  
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

bot.polling(none_stop = True, timeout = 30)
    
