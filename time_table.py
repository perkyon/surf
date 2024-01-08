import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Настройка доступа к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_credentials.json", scope)
client = gspread.authorize(creds)

# Открытие таблицы
sheet = client.open("График работы SC x post").sheet1

# Получение данных
rows = sheet.get_all_records()

# Функция отправки сообщений в Telegram
def send_telegram_message(chat_id, message):
    token = '6746134454:AAHvuB_hSpTWLJ1j1CET678aQhsrCWrRHAI'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, json=payload)

# Проверка и отправка уведомлений
for row in rows:
    date = datetime.strptime(row['Дата'], '%d.%m.%Y')
    if date.date() == datetime.now().date():
        message = f"У вас сегодня смена, {row['Имя']}"
        send_telegram_message(row['Telegram ID'], message)
