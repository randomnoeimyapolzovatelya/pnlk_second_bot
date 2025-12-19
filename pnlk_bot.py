import os
import telebot
from flask import Flask, request

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Создаем веб-сервер для работы на Render
app = Flask(__name__)

# Создаем список для хранения фильмов
movies = []

@app.route('/')
def index():
    return "Бот работает!"

# Этот эндпоинт будет принимать обновления от Telegram
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Функции-обработчики команд бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я работаю на Render.")

@bot.message_handler(commands=['add_film'])
def add_film(message):
    # Получаем текст сообщения после команды
    try:
        film_name = message.text.split(' ', 1)[1]
        if film_name:
            # Добавляем фильм в список
            movies.append(film_name)
            bot.reply_to(message, f"Фильм '{film_name}' успешно добавлен!")
        else:
            bot.reply_to(message, "Пожалуйста, укажите название фильма после команды.")
    except IndexError:
        bot.reply_to(message, "Не указано название фильма. Используйте: /add_film Название фильма")

@bot.message_handler(commands=['show_films'])
def show_films(message):
    if movies:
        film_list = '\n'.join([f"- {film}" for film in movies])
        bot.reply_to(message, f"Список фильмов:\n{film_list}")
    else:
        bot.reply_to(message, "Список фильмов пуст.")

@bot.message_handler(commands=['first'])
def send_welcome(message):
    bot.reply_to(message, "first")

@bot.message_handler(commands=['Первый'])
def send_welcome(message):
    bot.reply_to(message, "Первый")

# Запуск приложения
if __name__ == "__main__":
    # Удаляем старый вебхук и устанавливаем новый
    bot.remove_webhook()
    # Важно: URL здесь нужно будет заменить на ваш после деплоя
    # bot.set_webhook(url='https://ВАШ_ПРОЕКТ.onrender.com/' + BOT_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
