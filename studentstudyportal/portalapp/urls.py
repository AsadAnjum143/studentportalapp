from django.urls import path
from portalapp import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('notes/',views.notes, name = "notes"),
    path('delete_note/<int:pk>',views.delete_note, name = 'delete'),
    path('notes_details/<int:pk>',views.NotesDetailView.as_view(), name = "notes-details"),
    path('homework/',views.homework, name = "homework"),
    path('update_notes/',views.UpdateView.as_view(), name = "update"),
    path('delete_homework/<int:pk>',views.delete_homework, name = 'delete-homework'),
    path('update_homework/<int:pk>',views.update_homework, name = 'update-homework'),
    path('youtube/',views.youtube, name = 'youtube'),
    path('todo/',views.todo, name = 'todo'),
    path('delete_todo/<int:pk>',views.delete_todo, name = 'delete-todo'),
    path('update_todo/<int:pk>',views.update_todo, name = 'update-todo'),
    path('books/',views.book, name = 'book'),
    path('dictionary/',views.dictionary, name = 'dictionary'),
    path('wiki/',views.wiki, name = 'wiki'),
    path('conversion/',views.conversion, name = 'conversion'),
    
    
    
    
]