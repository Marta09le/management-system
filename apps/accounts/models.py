from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models


# Менеджер користувачів для налаштування користувачів в системі
class UserManager(BaseUserManager):
    # Приватний метод для створення користувача
    def _create_user(self, email, password, **extra_fields):
        # Перевірка, чи вказана електронна адреса
        if not email:
            raise ValueError('Users must have an email address')
        # Створення об'єкта користувача
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Метод для створення звичайного користувача
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', False)
        return self._create_user(email, password, **extra_fields)

    # Метод для створення менеджера
    def create_manager(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', True)
        return self._create_user(email, password, **extra_fields)

    # Метод для створення суперкористувача
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

    # Метод для отримання користувача за натуральним ключем (електронна пошта)
    def get_by_natural_key(self, email):
        return self.get(email=email)

# Модель групи користувачів
class GroupModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_group'

    def __str__(self):
        return self.name

    # Метод для підрахунку кількості користувачів в групі
    def users_count(self):
        return self.users.all().count()

    # Метод для підрахунку кількості нотаток в групі
    def notes_count(self):
        return NoteModel.objects.filter(group=self).count()

    # Метод для отримання всіх нотаток в групі
    def get_all_notes(self):
        return self.notes.all()

# Модель нотатки
class NoteModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name="notes")

    class Meta:
        db_table = 'note'

    # Метод для отримання дати створення нотатки
    def get_creation_date(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    # Метод для перевірки, чи належить нотатка користувачу
    def belongs_to_user(self, user):
        return self.group == user.group


# Модель користувача
class UserModel(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL,
                              related_name="users", null=True,
                              verbose_name="custom_user_groups")
    created = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    # Метод для отримання повного імені користувача
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Метод для отримання короткого імені користувача
    def get_short_name(self):
        return self.first_name

    # Метод для перевірки, чи є користувач членом вказаної групи
    def is_member_of_group(self, group_name):
        return self.group.name == group_name if self.group else False

    # Метод для відображення дозволів користувача
    def display_user_permissions(self):
        permissions = set(self.user_permissions.all())
        for group in self.groups.all():
            permissions |= set(group.permissions.all())
        return [perm.codename for perm in permissions]


