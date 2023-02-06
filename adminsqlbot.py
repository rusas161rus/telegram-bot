import psycopg2
from psycopg2 import Error
import requests as requests
from bs4 import BeautifulSoup
import config
import sqlconnect
import telebot
import logging
from telebot import types

logger=telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename = "log.log", format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot=telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def button(message):        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btm1 = types.KeyboardButton('Показать расписание')
    btm2 = types.KeyboardButton('Изменить расписание')
    btm3 = types.KeyboardButton('Обновить расписание в разработке')
    btm4 = types.KeyboardButton('Расписание с сайта РКСИ в разработке')           
    markup.add(btm1, btm3, btm2, btm4)
    bot.send_message(message.chat.id, 'Бот запущен!', reply_markup = markup)

@bot.message_handler(content_types = ['text', 'document', 'photo', 'audio', 'video', 'voice']) 
def send_text(message):

    if message.text == 'Расписание с сайта':
        while True:
            try:
                if __name__ == '__main__':
                    url = 'https://rksi.ru/mobile_schedule'
                    data = 'group=%C8%D1-11&stt=%CF%EE%EA%E0%E7%E0%F2%FC%21'
                    headers = {'Content-Type': 'application/x-www-form-urlencoded',
                            'Accept': 'text/html; charset=windows-1251'}
                    r = requests.post(url, data=data, headers=headers)
                    soup = BeautifulSoup(r.text, "html.parser")
                    classList = soup.findAll('p')
                    for cls in classList:
                        print(cls)
                
            except AttributeError:
                bot.send_message(message.chat.id, 'Попробуйте снова! Нажмите кнопку "Файл"')                
            else:
                bot.send_message(message.chat.id, classList)
            finally:
                break

    if message.text == 'Показать расписание':
        try: 
            connection = psycopg2.connect(  user = sqlconnect.USER, 
                                            password = sqlconnect.PASSWORD, 
                                            host = sqlconnect.HOST, 
                                            port = sqlconnect.PORT, 
                                            database = sqlconnect.DATABASE)
            cursor = connection.cursor()                              
            cursor.execute("SELECT * from Raspisanie".format(message.text))
            connection.commit()            
            record = cursor.fetchall()
            for row in record:
                a = str(row[0])
                b = str(row[1])
                c = str(row[2])
                d = str(row[3])
                e = str(row[4])                                 
                f = str(row[5])
                g = str(row[6])                
                raspis=(" | ИД=" + a + ", | Дата =" + b + ",\n\n | Время начала =" + c + ", | Время конца =" + d + ",\n\n | Предмет =" + e + ", | Преподователь =" + f + ",\n\n | Кабинет =" + g)
                #print("ИД =", row[0], "| Дата =", row[1], "| Время начала =", row[2], "| Время конца =", row[3], "| Предмет =", row[4], "| Преподователь =", row[5], "| Кабинет =", row[6])                      
                bot.send_message(message.chat.id, raspis)
        finally:                        
            if connection:                           
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")  
                
    if message.text == 'Изменить расписание':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Время Начала", callback_data = 'a'))
        markup.add(types.InlineKeyboardButton("Время Конца", callback_data = 'b'))
        markup.add(types.InlineKeyboardButton("Дата", callback_data = 'c'))
        markup.add(types.InlineKeyboardButton("Предмет", callback_data = 'd'))
        markup.add(types.InlineKeyboardButton("Учитель", callback_data = 'e'))
        markup.add(types.InlineKeyboardButton("Кабинет", callback_data = 'f'))
        markup.add(types.InlineKeyboardButton("Удалить запись", callback_data = 'g'))    
        markup.add(types.InlineKeyboardButton("Создать целую запись", callback_data = 'k'))
        #markup.add(types.InlineKeyboardButton("Обновить целую запись", callback_data = 'l'))    
        bot.send_message(message.chat.id, "Выберете кнопку", reply_markup = markup) 

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'a':
         markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Начало')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и замените x на свои значения\n\n 'xx:xx' where id = x")
         bot.register_next_step_handler(msg, create_request_1)
    if call.data == 'b':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Конец')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и замените x на свои значения\n\n 'xx:xx' where id = x")
         bot.register_next_step_handler(msg, create_request_2)
    if call.data == 'c':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Дата')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и подставьте свои значения\n\n 'гггг-мм-дд' where id = x")
         bot.register_next_step_handler(msg, create_request_3)
    if call.data == 'd':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Предмет')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и введите название предмета\n\n 'xxxxx' where id = x")
         bot.register_next_step_handler(msg, create_request_4)
    if call.data == 'e':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Учитель')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и введите имя учителя\n\n 'xxxxx' where id = x")
         bot.register_next_step_handler(msg, create_request_5)
    if call.data == 'f':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Кабинет')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте строчку и введите номер кабинета\n\n 'xxx' where id = x")
         bot.register_next_step_handler(msg, create_request_6)
    if call.data == 'g':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Удалить запись')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Введите ID записи")
         bot.register_next_step_handler(msg, create_request_7)
    if call.data == 'k':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Создать целую запись')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте текст и подставьте свои значения (ИД, Дата, Время начала, Время конца, предмет, преподователь, кабинет) \n\n 3, '2001.04.12', '18:30', '17:00', 'литература', 'Антонов', 203")
         bot.register_next_step_handler(msg, create_request_8)
    '''if call.data == 'l':
         markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True)
         bbtm_in = types.KeyboardButton('Обновить целую запись')
         markup_reply.add(bbtm_in)
         msg = bot.send_message(call.message.chat.id, "Скопируйте текст и подставьте свои значения (ИД, Дата, Время начала, Время конца, предмет, преподователь, кабинет) \n\n 3, '2001.04.12', '18:30', '17:00', 'литература', 'Антонов', 203")
         bot.register_next_step_handler(msg, create_request_9)'''


def create_request_1(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set TIME_S = {}""".format(message.text))
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

def create_request_2(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        cursor = connection.cursor()              
        cursor.execute("""Update Raspisanie set TIME_P = {}""".format(message.text))
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
        cursor.execute("""Update Raspisanie set DATE = {}""".format(message.text))
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

def create_request_4(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set PREDMET = {}""".format(message.text))
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

def create_request_5(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set PREPODOVATEL = {}""".format(message.text))
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

def create_request_6(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set KABINET = {}""".format(message.text))
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

def create_request_7(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)            
        cursor = connection.cursor()                              
        cursor.execute("""Delete from Raspisanie where id = ('{}')""".format(message.text))
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

def create_request_8(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)            
        cursor = connection.cursor()                              
        cursor.execute("""INSERT INTO Raspisanie (ID, DATE, TIME_S, TIME_P, PREDMET, PREPODOVATEL, KABINET) VALUES ({})""".format(message.text))
        connection.commit()
        print(cursor.rowcount, "1 Запись успешно Вставлена")        
        bot.send_message(message.chat.id, "1 Запись успешно Вставлена".format(name = message.text))  
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

'''def create_request_9(message):    
    try: 
        connection = psycopg2.connect(  user = sqlconnect.USER, 
                                        password = sqlconnect.PASSWORD, 
                                        host = sqlconnect.HOST, 
                                        port = sqlconnect.PORT, 
                                        database = sqlconnect.DATABASE)            
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set ID, DATE, TIME_S, TIME_P, PREDMET, PREPODOVATEL, KABINET VALUES ({})""".format(message.text))
        connection.commit()
        print(cursor.rowcount, "1 Запись успешно обновлена")        
        bot.send_message(message.chat.id, "1 Запись успешно обновлена".format(name = message.text))  
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто") ''' 



bot.polling(none_stop = True, timeout = 30)

