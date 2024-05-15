# Використання базового образу Python
FROM python:3.11

# Встановлення робочої директорії в контейнері
WORKDIR /app

# Створення користувача для безпеки
RUN useradd -m myuser
USER myuser

# Копіювання лише файлу з залежностями
COPY requirements.txt .

# Встановлення залежностей з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання решти файлів проекту в контейнер
COPY --chown=myuser:myuser . .

# Встановлення порту, на якому буде працювати застосунок
EXPOSE 8000

# Команда для запуску застосунку
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
