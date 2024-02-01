from datetime import datetime, timedelta

# Цветы и опрыскивание
spray_schedule = {
    "Юкка": {
        "interval": 2,
        "last_watered": datetime.now() - timedelta(days=2),
        "message": "Опрыскать Юкку"
    },
    "Драцена": {
        "interval": 3,
        "last_watered": datetime.now() - timedelta(days=3),
        "message": "Проверить Драцену и опрыскать по необходимости"
    },
    "Цикас": {
        "interval": 5,
        "last_watered": datetime.now() - timedelta(days=5),
        "message": "Открыть и проветрить укрытую пальму (Цикас) на улице"
    }
}

# Время для напоминаний
report_reminder_times = {
    "weekday": ["15:30", "23:00"],
    "weekend": ["16:30", "23:00"]
}

cleanliness_check_intervals = {
    "weekday": [(hour, 0) for hour in range(8, 20, 2)],  # Каждые 2 часа с 8:00 до 20:00
    "weekend": [(hour, 0) for hour in range(10, 18, 2)]  # Каждые 2 часа с 10:00 до 18:00
}

daily_task_times = {
    "weekday": ["08:00", "14:00", "20:00"],
    "weekend": ["09:00", "15:00"]
}

# Список задач на неделю с добавлением статуса выполнения
weekly_tasks = {
    "понедельник": [
        {"task": "Чистка гриндера", "completed": False},
        {"task": "Чистка гейзеров", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "вторник": [
        {"task": "Протереть лайт боксы и вывески", "completed": False},
        {"task": "Вымести листья и мусор под трибуны", "completed": False},
        {"task": "Натереть зеркала", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "среда": [
        {"task": "Чистка гриля и микроволновки", "completed": False},
        {"task": "Заточка ножей", "completed": False},
        {"task": "Протереть пыль (картины, батареи, полки)", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "четверг": [
        {"task": "Уборка на складе", "completed": False},
        {"task": "Чистка гриндера", "completed": False},
        {"task": "Зона витрины (убрать все подносы и замыть, натереть витрину внутри)", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "пятница": [
        {"task": "Протереть лайт боксы, гирлянду и вывеску", "completed": False},
        {"task": "Зона шкафов на баре (протереть полки, расставить продукцию, пополнить необходимое)", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "суббота": [
        {"task": "Чистка термопода кафизой", "completed": False},
        {"task": "Чистка блендера кафизой", "completed": False},
        {"task": "Протереть шкафы сверху", "completed": False},
        {"task": "Протереть духовку (стекло)", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ],
    "воскресенье": [
        {"task": "Почистить большой пылесос", "completed": False},
        {"task": "Протереть пыль (картины, батареи, полки)", "completed": False},
        {"task": "Протереть и помыть низ бара", "completed": False},
        {"task": "Замачивание форсунок и их чистка", "completed": False},
        {"task": "Протереть стекло входной двери", "completed": False}
    ]
}
