#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# Головна функція для виконання адміністративних завдань
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обробка помилки імпорту Django і виведення відповідного повідомлення
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    some_var = 0


# Якщо скрипт запускається напряму, викликається головна функція main()
if __name__ == '__main__':
    main()
