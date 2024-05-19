from django.urls import path
from . import views

# Визначення URL-шляхів для додатку
urlpatterns = [
    # Шлях для входу користувача
    path("login/", views.CustomLoginView.as_view(), name="login"),

# Шлях для реєстрації менеджера
    path("manager/create/", views.ManagerRegisterView.as_view(), name="manager-register"),
# Шлях для реєстрації користувача
    path("user/create/", views.UserRegisterView.as_view(), name="user-register"),
    # Шлях для виходу користувача
    path("logout/", views.CustomLogoutView.as_view(), name="logout")
]
