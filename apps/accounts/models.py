from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', False)
        return self._create_user(email, password, **extra_fields)

    def create_manager(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class GroupModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_group'

    def __str__(self):
        return self.name

    def users_count(self):
        return self.users.all().count()

    def notes_count(self):
        return NoteModel.objects.filter(group=self).count()

    def get_all_notes(self):
        return self.notes.all()


class NoteModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name="notes")

    class Meta:
        db_table = 'note'

    def get_creation_date(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    def belongs_to_user(self, user):
        return self.group == user.group


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

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def is_member_of_group(self, group_name):
        return self.group.name == group_name if self.group else False

    def display_user_permissions(self):
        permissions = set(self.user_permissions.all())
        for group in self.groups.all():
            permissions |= set(group.permissions.all())
        return [perm.codename for perm in permissions]


