from django.apps import AppConfig


# Клас конфігурації додатку Accounts
class AccountsConfig(AppConfig):
    # Вказуємо тип поля за замовчуванням для автоінкрементних первинних ключів
    default_auto_field = 'django.db.models.BigAutoField'
    # Ім'я додатку в проекті
    name = 'apps.accounts'
