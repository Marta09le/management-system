import logging

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts.forms import UserRegisterForm, UserLoginForm, ManagerRegisterForm

# Setting up a logger for this module.
logger = logging.getLogger(__name__)


# View for choosing the type of user to register (Manager or Regular User).
class ChooseWhoView(generic.TemplateView):
    template_name = 'choose_who.html'


# View for registering a manager.
class ManagerRegisterView(generic.CreateView):
    template_name = 'registration.html'
    form_class = ManagerRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user-list')

    # Custom form validation logic.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_manager = True  # Explicitly setting the user as a manager.
        self.object.set_password(form.cleaned_data['password'])  # Setting the password.

        self.object.save()
        return super().form_valid(form)

    # Adding additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Manager Registration'
        context['button_label'] = 'Create'
        context['is_manager'] = True
        return context


# View for registering a regular user.
class UserRegisterView(generic.CreateView):
    template_name = 'registration.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user-list')

    # Custom form validation logic.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_manager = False  # Explicitly setting the user as not a manager.
        self.object.set_password(form.cleaned_data['password'])  # Setting the password.
        group = form.cleaned_data.get('group', None)
        if group:
            self.object.group = group  # Setting the group if provided.

        self.object.save()
        return super().form_valid(form)

    # Adding additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Registration'
        context['button_label'] = 'Create'
        context['is_manager'] = False
        return context


# Custom login view.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    # Adding additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authorization'
        context['button_label'] = 'Login'

        # Logging when the login page context is prepared.
        logger.info("Отримано контекст для Manager Login")

        return context

    # Logging successful login attempts.
    def form_valid(self, form):
        logger.info(f"Успішна авторизація для користувача {form.get_user()}")
        return super().form_valid(form)

    # Logging failed login attempts.
    def form_invalid(self, form):
        logger.warning("Невдала спроба авторизації")
        return super().form_invalid(form)

    # Redirecting to a specific URL after successful login.
    def get_success_url(self):
        logger.info(f"Перенаправлення на {'user-list'}")
        return reverse_lazy('choose-list')


# Custom logout view.
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('choose-who')  # Redirecting to 'choose-who' page after logout.
