from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add_book/', views.add_book, name='add_book'),
    path('show_books/', views.show_books, name='show_books'),
    path('renew_book/<int:book_id>/', views.renew_book, name='renew_book'),
    path('my_transactions/', views.my_transactions, name='my_transactions'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('remove_book/<int:book_id>/', views.remove_book, name='remove_book'),
    path('reserve_book/<int:book_id>/', views.reserve_book, name='reserve_book'),
]