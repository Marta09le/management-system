from django.urls import path
from . import views

urlpatterns = [

    path('join-group/<int:pk>/', views.join_group, name='join-group'),

    path('note/', views.NoteListView.as_view(), name='note-list'),
    path('note/create/', views.NoteCreateView.as_view(), name='note-add'),
    path('note/edit/<int:pk>/', views.NoteUpdateView.as_view(), name='note-edit'),
    path('note/delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note-delete'),

]
