import os
import telebot

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Создаем веб-сервер для работы на Render
from flask import Flask, request
app = Flask(__name__)

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

# Запуск приложения
if __name__ == "__main__":
    # Удаляем старый вебхук и устанавливаем новый
    bot.remove_webhook()
    # Важно: URL здесь нужно будет заменить на ваш после деплоя
    # bot.set_webhook(url='https://ВАШ_ПРОЕКТ.onrender.com/' + BOT_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))