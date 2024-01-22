from datetime import datetime

# Время для напоминаний о написании отчетов
report_reminder_times = {
    "weekday": ["15:30", "23:00"],  # В будние дни
    "weekend": ["16:30", "23:00"]   # В выходные дни
}

# Время для напоминаний о проверке чистоты
cleanliness_check_intervals = {
    "weekday": [(hour, minute) for hour in range(7, 24, 2) for minute in (30,)],  # Каждые 2 часа с 7:30 до 23:00 в будние дни
    "weekend": [(hour, minute) for hour in range(9, 24, 2) for minute in (0,)]   # Каждые 2 часа с 9:00 до 23:00 в выходные дни
}

# Время для отправки списка задач на день
daily_task_times = {
    "weekday": ["07:30", "15:30", "23:00"],  # В будние дни
    "weekend": ["09:00", "16:30", "23:00"]   # В выходные дни
}

import logging

logging.basicConfig(level=logging.INFO)

def is_working_hour():
    now = datetime.now()
    logging.info(f"Текущее время: {now}")

# График работы
def is_working_hour():
    now = datetime.now()
    hour = now.hour
    if now.weekday() >= 5:  # Суббота или воскресенье
        return 9 <= hour < 23
    else:  # Будний день
        return 7 <= hour < 23