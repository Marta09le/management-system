import logging

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts.forms import UserRegisterForm, UserLoginForm, ManagerRegisterForm

# реєстрація користувачів
logger = logging.getLogger(__name__)


# Представлення для вибору типу користувача для реєстрації (Менеджер або Звичайний користувач).
class ChooseWhoView(generic.TemplateView):
    template_name = 'choose_who.html'


# Представлення для реєстрації менеджера.
class ManagerRegisterView(generic.CreateView):
    template_name = 'registration.html'
    form_class = ManagerRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user-list')

    # Кастомна логіка валідації форми для реєстрації менеджера.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_manager = True
        self.object.set_password(form.cleaned_data['password'])  # Встановлення паролю

        self.object.save()
        return super().form_valid(form)

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Manager Registration'
        context['button_label'] = 'Create'
        context['is_manager'] = True
        return context


# Представлення для реєстрації звичайного користувача.
class UserRegisterView(generic.CreateView):
    template_name = 'registration.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user-list')

    # Кастомна логіка валідації форми для реєстрації звичайного користувача.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_manager = False
        self.object.set_password(form.cleaned_data['password'])  # встановлення паролю
        group = form.cleaned_data.get('group', None)
        if group:
            self.object.group = group # Встановлюємо групу, якщо вона була вказана.

        self.object.save()
        return super().form_valid(form)

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Registration'
        context['button_label'] = 'Create'
        context['is_manager'] = False
        return context


# Кастомне представлення для входу в систему.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    # Додавання додаткового контексту до шаблону.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authorization'
        context['button_label'] = 'Login'

        # Логування підготовки контексту для сторінки входу.
        logger.info("Отримано контекст для Manager Login")

        return context

    # Логування успішних спроб входу.
    def form_valid(self, form):
        logger.info(f"Успішна авторизація для користувача {form.get_user()}")
        return super().form_valid(form)

    # Логування невдалих спроб входу.
    def form_invalid(self, form):
        logger.warning("Невдала спроба авторизації")
        return super().form_invalid(form)

    # Перенаправлення на певну URL після успішного входу.
    def get_success_url(self):
        logger.info(f"Перенаправлення на {'user-list'}")
        return reverse_lazy('choose-list')


# Кастомне представлення для виходу з системи.
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('choose-who')  # Перенаправлення на сторінку 'choose-who' після виходу.
