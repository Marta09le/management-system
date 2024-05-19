from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts.forms import UserLoginForm
# Представлення для стартової сторінки

class StartView(generic.TemplateView):
    template_name = 'start.html'    # Вказуємо шаблон для відображення цієї сторінки

# Представлення для вибору ролі користувача (хто буде реєструватися або входити)
class ChooseWhoView(generic.TemplateView):
    template_name = 'choose_who.html'   # Вказуємо шаблон для відображення цієї сторінки

