from dotenv import load_dotenv
from sys import exit as sexit
from os import remove, getenv

import telebot
import qrcode

# Загрузить переменные из файла .env
load_dotenv()
# Получить значение переменной
API_TOKEN = getenv("API_TOKEN")
if API_TOKEN is None:
    print('Отсутствует токен телеграм бота. Загрузи токен в переменные окружения и бот сможет начать работу')
    sexit(1)  # Завершаем программу с кодом ошибки 1


bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(mess):
    bot.send_message(mess.chat.id, 'Привет. Я генерирую QR коды. Отправь мне текст и я его преобразую')


def gen_qr(text):
    # Создаем экземпляр класса QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    # Добавляем данные в QR-код
    qr.add_data(text)
    qr.make(fit=True)
    # Создаем изображение QR-кода
    img = qr.make_image(fill_color="black", back_color="white")
    # Сохраняем изображение QR-кода
    img.save("qrcode.png")


@bot.message_handler(content_types=['text'])
def generate_qr_code(mess):
    gen_qr(mess.text)
    text = f'<b>Сообщение:</b> {mess.text}\n<b>Слов в сообщении:</b> {len(mess.text.split())}\n<b>Символов в сообщении:</b> {len(mess.text)}'
    with open('qrcode.png', 'rb') as qr_photo:
        bot.send_photo(mess.chat.id, qr_photo)
        bot.send_message(mess.chat.id, text, parse_mode='html')
    remove('qrcode.png')

print('Бот запущен')
bot.polling()
print('Бот отключён')