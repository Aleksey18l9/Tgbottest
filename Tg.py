import telebot
import os

# Загрузка токена из переменных окружения для безопасности
TOKEN = os.getenv('7281831571:AAFZgrlfndFI6Uz9hb5jxR9NfHy-c3cBIMA')  # Убедитесь, что вы установили эту переменную окружения
OWNER_ID = 7342810024
OWNER_NAME = '🎩'

# Файл для хранения числа
NUMBER_FILE = 'number.txt'

# Чтение числа из файла или установка значения по умолчанию
def read_number_from_file():
    try:
        with open(NUMBER_FILE, 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        # Если файл не найден или ошибка в чтении, возвращаем 0 и создаем файл
        with open(NUMBER_FILE, 'w') as file:
            file.write('0')
        return 0

# Запись числа в файл
def write_number_to_file(number):
    with open(NUMBER_FILE, 'w') as file:
        file.write(str(number))

# Инициализация бота и загрузка числа
bot = telebot.TeleBot(TOKEN)
users = {}
number = read_number_from_file()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global number
    bot.reply_to(message, f"Добро пожаловать, {message.from_user.first_name}! Число из файла: {number}")
    users[message.from_user.id] = message.from_user.username

@bot.message_handler(commands=['join'])
def join_server(message):
    if message.from_user.id not in users:
        users[message.from_user.id] = message.from_user.username
        bot.reply_to(message, "Вы успешно присоединились к серверу!")
    else:
        bot.reply_to(message, "Вы уже присоединились к серверу.")

@bot.message_handler(commands=['users'])
def list_users(message):
    if users:
        user_list = "\n".join([f"{user_id}: {username}" for user_id, username in users.items()])
        bot.reply_to(message, f"Список пользователей:\n{user_list}")
    else:
        bot.reply_to(message, "На сервере пока нет пользователей.")

@bot.message_handler(commands=['increment'])
def increment_number(message):
    """Команда для увеличения числа и сохранения его в файл."""
    global number
    number += 1
    write_number_to_file(number)
    bot.reply_to(message, f"Число увеличено: {number}")

print("Бот успешно запущен.")
bot.infinity_polling()
