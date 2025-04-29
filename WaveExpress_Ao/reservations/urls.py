from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.schedule_search, name='schedule_search'),
    path('book/<int:schedule_id>/', views.create_reservation, name='create_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
]
