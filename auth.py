import telebot
import sqlite3
from PIL import Image

# Создаем экземпляр бота
bot = telebot.TeleBot('5115885214:AAF8KYpo7PAfTHUzC_iMjLv1b-MGicOd32o')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Добро пожаловать! Выберите личность:')
    conn = sqlite3.connect("bfm_db.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            name, 
            surname 
        FROM 
            persons;
    """)
    exists = cursor.fetchall()
    for i in exists:
        bot.send_message(message.chat.id, ' '.join(i))
    cursor.close()

@bot.message_handler(content_types=["text"])
def handle_text(message):
    conn = sqlite3.connect("bfm_db.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            b.photo, 
            b.author, 
            b.title, 
            b.link
        FROM 
            books AS b
        JOIN 
            persons AS p
        ON 
            p.id = b.person_id
        WHERE 
            p.name = '{message.text.split()[0]}'
        AND
           p.surname = '{message.text.split()[1]}';
    """)
    exists = cursor.fetchall()
    bot.send_message(message.chat.id, f'{exists[0][1]}\n{exists[0][2]}\n{exists[0][3]}')
    cursor.close()

# Запускаем бота
bot.polling(none_stop=True, interval=0)