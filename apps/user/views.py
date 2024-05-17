from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts.forms import NoteAddForm
from apps.accounts.models import GroupModel, NoteModel


# Функція для приєднання до групи
@login_required
def join_group(request, pk):
    # Отримання групи або виведення помилки 404, якщо групу не знайдено
    group = get_object_or_404(GroupModel, id=pk)
    user = request.user

    # Перевірка, чи користувач вже не знаходиться у цій групі
    if user.group != group:
        user.group = group
        user.save()
        # Повідомлення про успішне приєднання до групи
        messages.success(request, f"Ви приєдналися {group.name}")
    else:
        # Повідомлення про те, що користувач вже в цій групі
        messages.info(request, "Ви вже в цій групі")
    # Перенаправлення на список нотаток
    return redirect('note-list')


# Клас для перегляду списку нотаток
class NoteListView(generic.ListView):
    model = NoteModel
    template_name = 'note_list.html'

    # Визначення набору даних для перегляду
    def get_queryset(self):
        user_group = self.request.user.group
        return NoteModel.objects.filter(group=user_group)

    # Перевірка автентифікації користувача
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Ви не маєте дозволу")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

# Клас для створення нотаток
class NoteCreateView(generic.CreateView):
    model = NoteModel
    form_class = NoteAddForm
    template_name = 'note_edit.html'
    success_url = reverse_lazy('group-list')

    # Додавання додаткових даних до контексту шаблону
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Створити нотатку'
        context['button_label'] = 'Створити'
        return context

    # Встановлення групи для нової нотатки
    def form_valid(self, form):
        form.instance.group = self.request.user.group
        return super().form_valid(form)

    # Перевірка автентифікації користувача
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Ви не маєте дозволу")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

# Клас для оновлення нотаток
class NoteUpdateView(generic.UpdateView):
    model = NoteModel
    form_class = NoteAddForm
    template_name = 'note_edit.html'
    success_url = reverse_lazy('note-list')

    # Додавання додаткових даних до контексту шаблону
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагувати примітку'
        context['button_label'] = 'Зберегти зміни'
        return context

    # Перевірка автентифікації користувача
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Ви не маєте дозволу")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

# Клас для видалення нотаток
class NoteDeleteView(generic.DeleteView):
    model = NoteModel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('note-list')

    # Додавання додаткових даних до контексту шаблону
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = False
        return context

        # Запобігання видаленню груп, які використовуються іншими об'єктами

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Цю групу неможливо видалити, оскільки вона використовується іншими об’єктами.")
            return redirect('some_view')

    # Перевірка автентифікації користувача
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Ви не маєте дозволу")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
