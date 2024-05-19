from django.urls import path
from . import views

# Визначення URL-шляхів для додатку
urlpatterns = [
# Шлях для приєднання до групи за ідентифікатором (pk)
    path('join-group/<int:pk>/', views.join_group, name='join-group'),
    # Шлях для відображення списку нотаток
    path('note/', views.NoteListView.as_view(), name='note-list'),
    # Шлях для створення нової нотатки
    path('note/create/', views.NoteCreateView.as_view(), name='note-add'),
# Шлях для редагування нотатки за ідентифікатором (pk)
    path('note/edit/<int:pk>/', views.NoteUpdateView.as_view(), name='note-edit'),
# Шлях для видалення нотатки за ідентифікатором (pk)
    path('note/delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note-delete'),

]
