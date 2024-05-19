
from django.apps import AppConfig


# Клас конфігурації додатку User
class UserConfig(AppConfig):
    # Вказуємо тип поля за замовчуванням для автоінкрементних первинних ключів
    default_auto_field = 'django.db.models.BigAutoField'
    # Ім'я додатку в проекті
    name = 'apps.user'
