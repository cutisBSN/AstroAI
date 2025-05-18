import os
import time
from datetime import datetime
import openai
import telebot
import schedule
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('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')
TG_BOT_TOKEN = os.getenv('7905213410:AAFfqzCRs6V5l_VvAlZcwbOVQRHfM0J2g5Q')
CHANNEL_ID = os.getenv('@newsfromopenai')
POST_TIME = os.getenv('POST_TIME', "08:00")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TG_BOT_TOKEN)

ZODIAC_SIGNS = [
    'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
    'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]

def get_astro_forecast(sign):
    prompt = (
        f"Напиши астрологический прогноз на ближайшие 24 часа для знака зодиака {sign}. "
        "Прогноз должен быть коротким (2-3 предложения), интересным, без политики и негатива. "
        "Добавь эмодзи по теме. Не упоминай дату и не дублируй текст из других прогнозов."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=180,
    )
    return response.choices[0].message.content.strip()

def send_daily_forecasts():
    today = datetime.now().strftime('%d.%m.%Y')
    header = f"🌟 Астрологический прогноз на ближайшие 24 часа для каждого знака зодиака ({today}):"
    bot.send_message(CHANNEL_ID, header)
    time.sleep(1)
    for sign in ZODIAC_SIGNS:
        try:
            forecast = get_astro_forecast(sign)
            post = f"**{sign}**\n{forecast}"
            bot.send_message(CHANNEL_ID, post, parse_mode="Markdown")
            print(f"{datetime.now()}: {sign} — отправлен")
            time.sleep(3)  # чтобы не забанили за спам
        except Exception as e:
            print(f"Ошибка при отправке {sign}: {e}")

def job():
    print(f"{datetime.now()}: Запускается публикация астропрогнозов")
    send_daily_forecasts()

if __name__ == '__main__':
    schedule.every().day.at(POST_TIME).do(job)
    print("Астро-бот автопостер запущен!")
    while True:
        schedule.run_pending()
        time.sleep(10)
