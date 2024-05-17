

from django.db import migrations, models
import django.db.models.deletion

# Оголошення класу міграції, який буде виконувати зміни в базі даних
class Migration(migrations.Migration):
    initial = True

    # Визначаємо залежності цієї міграції від інших міграцій
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]
    # Описуємо операції, які будуть виконані цією міграцією
    operations = [
        # Створення моделі GroupModel
        migrations.CreateModel(
            name="GroupModel",
            fields=[
                # Поле id - первинний ключ, автоматично створюваний
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                # Поле name - унікальне поле з максимальною довжиною 20 символів
                ("name", models.CharField(max_length=20, unique=True)),
                # Поле description - поле з максимальною довжиною 20 символів
                ("description", models.CharField(max_length=20)),
                # Поле created - дата і час створення, автоматично додається при створенні запису
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            # Вказуємо ім'я таблиці в базі даних
            options={
                "db_table": "user_group",
            },
        ),
        # Створення моделі NoteModel
        migrations.CreateModel(
            name="NoteModel",
            fields=[
                # Поле id - первинний ключ, автоматично створюваний
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                # Поле name - поле з максимальною довжиною 50 символів
                ("name", models.CharField(max_length=50)),
                # Поле description - поле з максимальною довжиною 50 символів
                ("description", models.CharField(max_length=50)),
                # Поле created - дата і час створення, автоматично додається при створенні запису
                ("created", models.DateTimeField(auto_now_add=True)),
                # Поле group - зовнішній ключ, який зв'язує NoteModel з GroupModel
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to="accounts.groupmodel",
                    ),
                ),
            ],
            # Вказуємо ім'я таблиці в базі даних
            options={
                "db_table": "note",
            },
        ),
        # Створення моделі UserModel
        migrations.CreateModel(
            name="UserModel",
            fields=[
                # Поле id - первинний ключ, автоматично створюваний
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                # Поле password - поле для зберігання пароля
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                # Поле is_superuser - поле для позначення суперкористувача
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("is_manager", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="users",
                        to="accounts.groupmodel",
                        verbose_name="custom_user_groups",
                    ),
                ),
                # Поле groups - багатозначне поле для зберігання груп користувача
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="custom_user_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                # Поле user_permissions - багатозначне поле для зберігання дозволів користувача
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="custom_user_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            # Вказуємо ім'я таблиці в базі даних
            options={
                "db_table": "user",
            },
        ),
    ]
