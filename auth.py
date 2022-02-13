import telebot
import sqlite3
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('5115885214:AAF8KYpo7PAfTHUzC_iMjLv1b-MGicOd32o')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    msg = bot.send_message(message.chat.id, 'Добро пожаловать!')
    bot.register_next_step_handler(message, buttons(message))

def buttons(message):
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
    keyboard = types.InlineKeyboardMarkup()
    print(exists)
    for i in exists:
        keyboard.add(types.InlineKeyboardButton(text=f'{i[0]} {i[1]}', callback_data=f'{i[0]} {i[1]}'))
    bot.send_message(message.chat.id, 'Выберите личность, '
                                      'рекомендации которого вы хотели бы посмотреть:', reply_markup=keyboard)
    cursor.close()

def return_button(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'hgfjfgjhgf', callback_data=f'ghfjjghj'))
    bot.send_message(message.chat.id, '', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    print(call.data.split()[0])
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
            p.name = '{call.data.split()[0]}'
        AND
           p.surname = '{call.data.split()[1]}';
    """)
    exists = cursor.fetchall()
    bot.send_message(call.message.chat.id, f'{call.data} рекомендует:')
    for desc in exists:
        bot.send_message(call.message.chat.id, f'*{desc[1]}\n{desc[2]}*\n[Ссылка]({desc[3]})', parse_mode='Markdown')
    cursor.close()

# Запускаем бота
bot.polling(none_stop=True, interval=0)