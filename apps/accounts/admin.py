from django.contrib import admin
from .models import UserModel, GroupModel, NoteModel


# Реєстрація моделі UserModel у адміністративному інтерфейсі
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    # Визначаємо поля, які будуть відображатися у списку користувачів
    list_display = ('email', 'first_name', 'last_name', 'is_manager')

    list_filter = ('is_manager',)
    # Визначаємо поля, за якими можна здійснювати пошук користувачів
    search_fields = ('email', 'first_name', 'last_name')


# Реєстрація моделі GroupModel у адміністративному інтерфейсі
@admin.register(GroupModel)
# Визначаємо поля, які будуть відображатися у списку групІ
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Реєстрація моделі NoteModel у адміністративному інтерфейсі
@admin.register(NoteModel)
class NoteAdmin(admin.ModelAdmin):
    # Визначаємо поля, які будуть відображатися у списку нотаток
    list_display = ('name', 'description', 'created', 'group')

    list_filter = ('group',)
    # Визначаємо поля, за якими можна здійснювати пошук нотаток
    search_fields = ('name', 'description')
