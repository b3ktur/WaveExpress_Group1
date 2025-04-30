from django.urls import path
from . import views
from . import reservation_views

app_name = 'ferry_system'

urlpatterns = [
    # Schedule URL
    path('schedules/', views.schedule_list, name='schedule_list'),
    
    # Reservation URLs (Transaction #2: A passenger reserves a ticket)
    path('reservations/reserve/<int:schedule_id>/', reservation_views.reserve_ticket, name='reserve_ticket'),
    path('reservations/pay/<int:reservation_id>/', reservation_views.pay_reservation, name='pay_reservation'),
    path('reservations/payment-in-progress/<int:reservation_id>/', reservation_views.payment_in_progress, name='payment_in_progress'),
    path('reservations/confirmation/<int:reservation_id>/', reservation_views.reservation_confirmation, name='reservation_confirmation'),
    path('reservations/detail/<int:reservation_id>/', reservation_views.reservation_detail, name='reservation_detail'),
    path('reservations/cancel/<int:reservation_id>/', reservation_views.cancel_reservation, name='cancel_reservation'),
    path('reservations/convert/<int:reservation_id>/', reservation_views.convert_to_ticket, name='convert_to_ticket'),
    path('reservations/my-reservations/', reservation_views.my_reservations, name='my_reservations'),
]
