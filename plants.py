from datetime import datetime, timedelta

# Цветы и опрыскивание 
spray_schedule = {
    "Юкка": {"interval": 2, "last_watered": datetime.now() - timedelta(days=2), "message": "Опрыскать Юкку"},
    "Драцена": {"interval": 2, "last_watered": datetime.now() - timedelta(days=2), "message": "Проверить Драцену (Саня и Мия) и опрыскать по необходимости"},
    "Цикас": {"interval": 2, "last_watered": datetime.now() - timedelta(days=2), "message": "Открыть и проветрить укрытую пальму (Цикас) на улице"}
}
