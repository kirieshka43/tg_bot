import telegram
from telegram import Updater, CommandHandler, MessageHandler, Filters
import datetime

# Замените "YOUR_BOT_TOKEN" на токен вашего бота
TOKEN = "6160888297:AAH5KdnfEt0aPINbu8KwzwaQKhqJB3qjoAI"

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот 'Письмо в будущее'. Пожалуйста, отправь мне текстовое сообщение, которое я доставлю в будущем.")

# Обработчик текстового сообщения
def send_message(update, context):
    now = datetime.datetime.now()
    future_date = now + datetime.timedelta(days=365)  # Дата, на которую отправить письмо (1 год вперед)

    message = update.message.text
    chat_id = update.effective_chat.id

    context.job_queue.run_once(send_future_message, future_date, context=(chat_id, message))

    context.bot.send_message(chat_id=chat_id, text="Я доставлю это сообщение в будущее.")

# Функция для отправки сообщения в будущем
def send_future_message(context):
    job = context.job
    chat_id, message = job.context

    context.bot.send_message(chat_id=chat_id, text=f"Ваше сообщение из прошлого: {message}")

# Создание экземпляра Updater и добавление обработчиков команд
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = MessageHandler(Filters.text, send_message)
dispatcher.add_handler(message_handler)

# Запуск бота
updater.start_polling()