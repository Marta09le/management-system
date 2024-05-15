from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),

    path("manager/create/", views.ManagerRegisterView.as_view(), name="manager-register"),

    path("user/create/", views.UserRegisterView.as_view(), name="user-register"),

    path("logout/", views.CustomLogoutView.as_view(), name="logout")
]
