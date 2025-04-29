from django.urls import path
from . import views
from . import ticket_views

app_name = 'ferry_system'

urlpatterns = [
    # Schedule and ticket URLs (Transaction #1: Passenger buys a ticket)
    path('schedules/', ticket_views.schedule_list, name='schedule_list'),
    path('tickets/buy/<int:schedule_id>/', ticket_views.buy_ticket, name='buy_ticket'),
    path('tickets/pay/<int:ticket_id>/', ticket_views.pay_ticket, name='pay_ticket'),
    path('tickets/confirmation/<int:ticket_id>/', ticket_views.ticket_confirmation, name='ticket_confirmation'),
    path('tickets/detail/<int:ticket_id>/', ticket_views.ticket_detail, name='ticket_detail'),
    path('tickets/print/<int:ticket_id>/', ticket_views.print_ticket, name='print_ticket'),
    path('tickets/cancel/<int:ticket_id>/', ticket_views.cancel_ticket, name='cancel_ticket'),
    path('tickets/my-tickets/', ticket_views.my_tickets, name='my_tickets'),
    
    # More URLs will be added for other transactions
]
