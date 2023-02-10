import psycopg2
from psycopg2 import Error
import requests as requests
import config
from bs4 import BeautifulSoup
import pyperclip
import telebot
import logging
from telebot import types
import schedule
from threading import Thread
from time import sleep

Admin_list = config.Admin_list

logger=telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename = "log.log", format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot=telebot.TeleBot(config.TOKEN)
my_chat_id = config.my_chat_id

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run():
    return bot.send_message(my_chat_id, "Звонок через 10 минут")
if __name__ == "__main__":
    schedule.every().day.at("07:50:00").do(function_to_run)
    schedule.every().day.at("09:30:00").do(function_to_run)
    schedule.every().day.at("11:20:00").do(function_to_run)
    schedule.every().day.at("13:00:00").do(function_to_run)
    schedule.every().day.at("14:50:00").do(function_to_run)
    schedule.every().day.at("16:30:00").do(function_to_run) 
    schedule.every().day.at("18:10:00").do(function_to_run)    
    Thread(target=schedule_checker).start() 

@bot.message_handler(commands = ['start'])
def button(message):        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btm6 = types.KeyboardButton('Сайт РКСИ и Ссылка на Облако с заданиями')
    markup.add(btm6)
    btm1 = types.KeyboardButton('Расписание')
    btm4 = types.KeyboardButton('Расписание с сайта РКСИ')
    btm5 = types.KeyboardButton('Поиск по времени')    
    markup.add(btm4, btm1, btm5)
    btm3 = types.KeyboardButton('Обновить расписание в базе')
    btm2 = types.KeyboardButton('Изменить расписание')               
    markup.add(btm3, btm2)
    bot.send_message(message.chat.id, 'Бот запущен!', reply_markup = markup)

@bot.message_handler(content_types = ['text', 'document', 'photo', 'audio', 'video', 'voice']) 
def send_text(message):

    if message.text=='Сайт РКСИ и Ссылка на Облако с заданиями':
        markup=types.InlineKeyboardMarkup(row_width=2)
        btm_ss_0 = types.InlineKeyboardButton("Облако с Заданиями", url="https://cloud.mail.ru/public/Tb2G/Fuc5s2Sks")
        btm_ss_1 = types.InlineKeyboardButton("Сайт РКСИ", url="https://www.rksi.ru/schedule")
        markup.add(btm_ss_0, btm_ss_1)
        bot.send_message(message.chat.id, 'Сайт РКСИ и Ссылка на Облако с заданиями!', reply_markup=markup)     

    if message.text == 'Обновить расписание в базе':
        while True:
            try:                
                
                id_message_user = message.from_user.id
            except ValueError:
                print("Обновить расписание в базе") 
            if id_message_user in Admin_list:
                try:
                    connection = psycopg2.connect(  user = config.USER, 
                                                    password = config.PASSWORD, 
                                                    host = config.HOST, 
                                                    port = config.PORT, 
                                                    database = config.DATABASE)        
                    file1 = open('pars.txt')
                    cursor = connection.cursor()
                    cursor.execute (''' DELETE FROM Raspisanie ''')    
                    cursor = connection.cursor()
                    file1 = open('pars.txt', 'r')   
                    for line in file1:
                        cursor.execute("""INSERT INTO Raspisanie (TIME_S, TIME_P, PREDMET, PREPODOVATEL, KABINET) VALUES {}""".format(line.strip()))
                        print(line)
                        #print("Line{}: {}".format(count, line.strip()))
                    connection.commit()
                    print(cursor.rowcount, "1 Запись успешно Вставлена")
                    bot.send_message(message.chat.id, "Расписание в базе успешно обновлено".format(message.from_user, bot.get_me()),
                    parse_mode = 'html')
                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)   
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("Соединение с PostgreSQL закрыто")
                        break    
            if id_message_user not in Admin_list:
                bot.send_message(message.chat.id, "Что бы обновить расписание нужно быть админом")
                break 

    if message.text == 'Расписание с сайта РКСИ':        
        with open ('pars.txt', 'w') as f:
            f.write('')      
            
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
                with open("pars.txt", "a") as file:
                    print(cls, file=file)
    
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace(", ", "', '")   
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("  —  ", "', '")   
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("<br/><b>", "', '") 
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("</b><br/>", "', '")  
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("<p>", "('") 
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("</p>", "')")   
        with open ('pars.txt', 'w') as f:
            f.write(new_data)
        with open ('pars.txt', 'r') as f:
            old_data = f.read()
        new_data = old_data.replace("""<a href="/">На сайт</a>""", "00:00', '00:00', '00:00', '00:00', '00:00") 
        with open ('pars.txt', 'w') as f:
            f.write(new_data)        
        
        with open("pars.txt") as file:
            data = file.read()
        pyperclip.copy(data)          

        bot.send_message(message.chat.id, data)  

    if message.text == 'Расписание':
        try: 
            connection = psycopg2.connect(  user = config.USER, 
                                            password = config.PASSWORD, 
                                            host = config.HOST, 
                                            port = config.PORT, 
                                            database = config.DATABASE)
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
                raspis=("|ИД=" + a + "|" + b + "|с-" + c + "|по-" + d + "\n\n|" + e + "|" + f + "|каб-" + g)
                #print("ИД =", row[0], "| Дата =", row[1], "| Время начала =", row[2], "| Время конца =", row[3], "| Предмет =", row[4], "| Преподователь =", row[5], "| Кабинет =", row[6])                      
                bot.send_message(message.chat.id, raspis)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
        finally:                        
            if connection:                           
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    if message.text == 'Поиск по времени':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btmin_s=types.InlineKeyboardButton("По Времени Начала", callback_data = 'nachalo')
        btmin_p=types.InlineKeyboardButton("По Времени Конца", callback_data = 'conec')
        markup.add(btmin_s, btmin_p)              
        bot.send_message(message.chat.id, "Нажмите кнопку!", reply_markup = markup)  
                
    if message.text == 'Изменить расписание':
        while True:
            try:                
                id_message_user = message.from_user.id                                                           
            except ValueError:
                print("что то пошло не так")                        
                continue        
            if id_message_user in Admin_list:
                markup = types.InlineKeyboardMarkup(row_width=3)
                markup.add(types.InlineKeyboardButton("Создать целую запись", callback_data = 'k'))
                btm_l_1 = types.InlineKeyboardButton("Время Начала", callback_data = 'a')
                btm_l_2 = types.InlineKeyboardButton("Время Конца", callback_data = 'b')
                markup.add(btm_l_1, btm_l_2)
                markup.add(types.InlineKeyboardButton("Дата", callback_data = 'c'))
                btm_l_3 = types.InlineKeyboardButton("Предмет", callback_data = 'd')
                btm_l_4 = types.InlineKeyboardButton("Учитель", callback_data = 'e')
                btm_l_5 = types.InlineKeyboardButton("Кабинет", callback_data = 'f')
                markup.add(btm_l_3, btm_l_4, btm_l_5)
                markup.add(types.InlineKeyboardButton("Удалить запись", callback_data = 'g')) 
                #markup.add(types.InlineKeyboardButton("Обновить целую запись", callback_data = 'l'))    
                bot.send_message(message.chat.id, "Выберете что хотите отредактировать", reply_markup = markup)
                break
            if id_message_user not in Admin_list:
                bot.send_message(message.chat.id, "Что бы менять расписание нужно быть админом")
                break    
                    
@bot.callback_query_handler(func = lambda call: True)
def answer(call):    
    if call.data == 'a': # Время Начала   
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_0)
    if call.data == 'b': # Время Конца      
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_1)
    if call.data == 'c': # Дата      
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_2)
    if call.data == 'd': # Предмет      
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_3)
    if call.data == 'e': # Учитель      
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_4)
    if call.data == 'f': # Кабинет     
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_message_5)
    if call.data == 'g': # Удалить запись      
        msg = bot.send_message(call.message.chat.id, "Введите ИД записи")
        bot.register_next_step_handler(msg, create_request_delete_1)
    if call.data == 'k': # Создать целую запись       
        msg = bot.send_message(call.message.chat.id, "Введите дату в формате гггг-мм-дд")
        bot.register_next_step_handler(msg, create_insrt_request_message_0)
    if call.data == 'nachalo':        
        msg = bot.send_message(call.message.chat.id, "Введите время начала с в формате хх:хх")
        bot.register_next_step_handler(msg, create_select_request_message_0)
    if call.data == 'conec':        
        msg = bot.send_message(call.message.chat.id, "Введите время конца с в формате хх:хх")
        bot.register_next_step_handler(msg, create_select_request_message_1)   

# Функция поиска по времени
def create_select_request_message_0(message):
    global text_select_ts_0
    text_select_ts_0 = message.text
    msg=bot.send_message(message.chat.id, "Введите время начала по в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, select_request_SQL_s_0)
def create_select_request_message_1(message):
    global text_select_tp_0
    text_select_tp_0 = message.text
    msg=bot.send_message(message.chat.id, "Введите время конца по в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, select_request_SQL_s_1)

# Добавление по 1 параметру
def create_request_message_0(message):
    global text_0
    text_0 = message.text
    msg=bot.send_message(message.chat.id, "Введите время начала в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s0)
def create_request_message_1(message):
    global text_1
    text_1 = message.text
    msg=bot.send_message(message.chat.id, "Введите время конца в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s1)
def create_request_message_2(message):
    global text_2
    text_2 = message.text
    msg=bot.send_message(message.chat.id, "Введите дату в формате гггг-мм-дд".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s2)
def create_request_message_3(message):
    global text_3
    text_3 = message.text
    msg=bot.send_message(message.chat.id, "Введите название урока".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s3)
def create_request_message_4(message):
    global text_4
    text_4 = message.text
    msg=bot.send_message(message.chat.id, "Введите Имя преподователя".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s4)
def create_request_message_5(message):
    global text_5
    text_5 = message.text
    msg=bot.send_message(message.chat.id, "Введите № кабинета".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s5)

# Функция пошагового добавления записи
def create_insrt_request_message_0(message):
    global text_insert_0
    text_insert_0 = message.text
    msg=bot.send_message(message.chat.id, "Введите время начала в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_insrt_request_message_s0)
def create_insrt_request_message_s0(message):
    global text_insert_1
    text_insert_1 = message.text
    msg=bot.send_message(message.chat.id, "Введите время конца в формате хх:хх".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_insrt_request_message_s1)
def create_insrt_request_message_s1(message):
    global text_insert_2
    text_insert_2 = message.text
    msg=bot.send_message(message.chat.id, "Введите название урока".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_insrt_request_message_s2)
def create_insrt_request_message_s2(message):
    global text_insert_3
    text_insert_3 = message.text
    msg=bot.send_message(message.chat.id, "Введите Имя преподователя".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_insrt_request_message_s3)
def create_insrt_request_message_s3(message):
    global text_insert_4
    text_insert_4 = message.text
    msg=bot.send_message(message.chat.id, "Введите № кабинета".format(message.from_user, bot.get_me()),
    parse_mode = 'html')            
    bot.register_next_step_handler(msg, create_request_SQL_s6)

def create_request_SQL_s0(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE) 
        text_only_one_0 = [text_0]       
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set TIME_S = '{}' where id = %s""".format(message.text), (text_only_one_0))
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
def create_request_SQL_s1(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_only_one_1 = [text_1]       
        cursor = connection.cursor()              
        cursor.execute("""Update Raspisanie set TIME_P = '{}' where id = %s""".format(message.text), (text_only_one_1))
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
def create_request_SQL_s2(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_only_one_2 = [text_2]
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set DATE = '{}' where id = %s""".format(message.text), (text_only_one_2))
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
def create_request_SQL_s3(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_only_one_3 = [text_3]
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set PREDMET = '{}' where id = %s""".format(message.text), (text_only_one_3))
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
def create_request_SQL_s4(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_only_one_4 = [text_4]
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set PREPODOVATEL = '{}' where id = %s""".format(message.text), (text_only_one_4))
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
def create_request_SQL_s5(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_only_one_5 = [text_5]
        cursor = connection.cursor()                              
        cursor.execute("""Update Raspisanie set KABINET = '{}' where id = %s""".format(message.text), (text_only_one_5))
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
def create_request_delete_1(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)            
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
def create_request_SQL_s6(message):    
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)        
        text_insert_5 = message.text
        text = [text_insert_0, text_insert_1, text_insert_2, text_insert_3, text_insert_4, text_insert_5]           
        cursor = connection.cursor()                              
        cursor.execute("""INSERT INTO Raspisanie (DATE, TIME_S, TIME_P, PREDMET, PREPODOVATEL, KABINET) VALUES (%s, %s, %s, %s, %s, %s)""".format(message.text), (text))
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
def select_request_SQL_s_0(message):
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_select_ts_1 = message.text
        time_s = [text_select_ts_0, text_select_ts_1]
        cursor = connection.cursor()                              
        cursor.execute("SELECT *   from raspisanie r  WHERE (time_s , time_s) OVERLAPS (%s::time , %s::time);", (time_s))
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
            raspis=("|ИД=" + a + "|" + b + "|с-" + c + "|по-" + d + "\n\n|" + e + "|" + f + "|каб-" + g)
            #print("ИД =", row[0], "| Дата =", row[1], "| Время начала =", row[2], "| Время конца =", row[3], "| Предмет =", row[4], "| Преподователь =", row[5], "| Кабинет =", row[6])                      
            bot.send_message(message.chat.id, raspis)
            bot.send_message(message.chat.id, "--------------------------------------------------------------".format(name = message.text))
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))                
    finally:                        
        if connection:                           
            cursor.close()
            connection.close()
            bot.send_message(message.chat.id, "Поиск завершен!".format(name = message.text))
            print("Соединение с PostgreSQL закрыто")
def select_request_SQL_s_1(message):
    try: 
        connection = psycopg2.connect(  user = config.USER, 
                                        password = config.PASSWORD, 
                                        host = config.HOST, 
                                        port = config.PORT, 
                                        database = config.DATABASE)
        text_select_tp_1 = message.text
        time_p = [text_select_tp_0, text_select_tp_1]
        cursor = connection.cursor()                              
        cursor.execute("SELECT *   from raspisanie r  WHERE (time_p , time_p) OVERLAPS (%s::time , %s::time);", (time_p))
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
            raspis=("|ИД=" + a + "|" + b + "|с-" + c + "|по-" + d + "\n\n|" + e + "|" + f + "|каб-" + g)
            #print("ИД =", row[0], "| Дата =", row[1], "| Время начала =", row[2], "| Время конца =", row[3], "| Предмет =", row[4], "| Преподователь =", row[5], "| Кабинет =", row[6])                      
            bot.send_message(message.chat.id, raspis)
            bot.send_message(message.chat.id, "--------------------------------------------------------------".format(name = message.text))            
    except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            bot.send_message(message.chat.id, "Ошибка при работе с PostgreSQL".format(name = message.text))
    finally:                        
        if connection:                           
            cursor.close()
            connection.close()
            bot.send_message(message.chat.id, "Поиск завершен!".format(name = message.text))
            print("Соединение с PostgreSQL закрыто")

bot.polling(none_stop = True, timeout = 30)

