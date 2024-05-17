from django.apps import AppConfig

# Оголошення класу конфігурації додатку, який успадковується від AppConfig
class AdminConfig(AppConfig):
    # Вказуємо тип поля, який буде використовуватися за замовчуванням для автоматично створюваних полів первинного ключа
    default_auto_field = 'django.db.models.BigAutoField'
    # Вказуємо ім'я додатку, яке буде використовуватися Django для пошуку додатку та його конфігурації
    name = 'apps.manager'
