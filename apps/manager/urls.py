from django.urls import path, include
from . import views

# Визначення списку URL-маршрутів для додатку
urlpatterns = [

    path('', views.ManagerListView.as_view(), name='manager-list'),

    path('choose-list/', views.ChooseListView.as_view(), name='choose-list'),


    path('user/', views.UserListView.as_view(), name='user-list'),
    path('user/edit/<int:pk>/', views.CustomUpdateView.as_view(), name='user-edit'),
    path('user/delete/<int:pk>/', views.CustomDeleteView.as_view(), name='user-delete'),

    # Маршрути для роботи з подіями (групами)
    path('event/', views.GroupListView.as_view(), name='group-list'),
    path('event/create/', views.GroupCreateView.as_view(), name='group-add'),
    path('event/edit/<int:pk>/', views.GroupUpdateView.as_view(), name='group-edit'),
    path('event/delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group-delete'),
    # Маршрут для відображення сторінки з помилкою
    path('error/', views.ErrorView.as_view(), name='error'),
    # Включення URL-маршрутів з додатку 'apps.accounts'
    path('', include('apps.accounts.urls')),


]
