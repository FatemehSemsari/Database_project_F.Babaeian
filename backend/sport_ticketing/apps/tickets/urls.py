from django.urls import path

from apps.tickets.views import search_tickets, ticket_detail


urlpatterns = [
    path("search/", search_tickets, name="ticket-search"),
    path("details/<int:ticket_category_id>/", ticket_detail, name="ticket-detail"),
]