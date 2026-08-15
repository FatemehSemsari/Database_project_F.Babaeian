from django.urls import path

from apps.tickets.views import search_tickets, ticket_details, my_bookings, cancellation_info, cancel_ticket


urlpatterns = [
    path("search/", search_tickets, name="ticket-search"),
    path("details/<int:ticket_category_id>/", ticket_details, name="ticket-detail"),
    path("my-bookings/", my_bookings, name="my-bookings"),
    path("<int:ticket_id>/cancellation-info/", cancellation_info, name="ticket-cancellation-info"),
    path("<int:ticket_id>/cancel/", cancel_ticket, name="ticket-cancel"),
]