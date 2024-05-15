from django.contrib import admin
from .models import UserModel, GroupModel, NoteModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_manager')
    list_filter = ('is_manager',)
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(GroupModel)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(NoteModel)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'group')
    list_filter = ('group',)
    search_fields = ('name', 'description')
