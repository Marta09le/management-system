from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from apps.accounts.forms import UserRegisterForm, GroupAddForm
from apps.accounts.models import UserModel, GroupModel, NoteModel


# Вибір між різними списками (користувачі або групи).
class ChooseListView(generic.TemplateView):
    template_name = 'choose_lists.html'


# Відображення списку звичайних користувачів.
class UserListView(generic.ListView):
    model = UserModel
    template_name = 'users_list.html'
    context_object_name = 'users'

    # Фільтрація вибірки для включення лише не-менеджерів.
    def get_queryset(self):
        return UserModel.objects.filter(is_manager=False)

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of users'
        context['button_label'] = 'Додати користувача'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.is_authenticated and not request.user.is_manager):
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# Відображення списку менеджерів.
class ManagerListView(generic.ListView):
    model = UserModel
    template_name = 'users_list.html'
    context_object_name = 'users'

    # Фільтрація вибірки для включення лише менеджерів.
    def get_queryset(self):
        return UserModel.objects.filter(is_manager=True)

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of managers'
        context['button_label'] = 'Додати менеджера'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_manager:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# Оновлення інформації користувача.
class CustomUpdateView(generic.UpdateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('user-list')

    # Перевірка дозволів перед дозволом редагування.
    def dispatch(self, request, *args, **kwargs):
        user_to_edit = get_object_or_404(UserModel, pk=kwargs['pk'])
        if not request.user.is_authenticated or (not request.user.is_manager and request.user != user_to_edit):
            messages.error(request, "You don't have permission to edit this profile.")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# Видалення користувача.
class CustomDeleteView(generic.DeleteView):
    model = UserModel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('user-list')

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = True
        return context

    # Перевірка дозволів перед дозволом видалення.
    def dispatch(self, request, *args, **kwargs):
        user_to_edit = get_object_or_404(UserModel, pk=kwargs['pk'])
        if not request.user.is_authenticated or (not request.user.is_manager and request.user != user_to_edit):
            messages.error(request, "You don't have permission to edit this profile.")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


#  ===========  REST URL METHOD  ===========

# Відображення списку груп.
class GroupListView(generic.ListView):
    model = GroupModel
    template_name = 'groups_list.html'
    context_object_name = 'groups'


# Створення нової групи.
class GroupCreateView(generic.CreateView):
    model = GroupModel
    form_class = GroupAddForm
    template_name = "edit_event.html"
    success_url = reverse_lazy('group-list')

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Створити подію'
        context['button_label'] = 'Створити'
        return context


# Оновлення інформації групи.
class GroupUpdateView(generic.UpdateView):
    model = GroupModel
    form_class = GroupAddForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('group-list')

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit event'
        context['button_label'] = 'Зберегти зміни'
        context['notes'] = NoteModel.objects.all()
        return context

    # Перевірка дозволів перед дозволом редагування.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# Видалення групи.
class GroupDeleteView(generic.DeleteView):
    model = GroupModel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('group-list')

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = False
        return context

    # Перевірка дозволів та членства в групі перед дозволом видалення.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)

    # Запобігання видаленню груп із членами.
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "This group cannot be deleted because it is used by other objects.")
            return redirect('some_view')


# Відображення повідомлення про помилку.
class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'error.html', {})



