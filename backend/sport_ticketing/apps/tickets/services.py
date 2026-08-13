from apps.tickets.repositories import TicketRepository
from apps.tickets.search_cache import (
    cache_ticket_search,
    get_cached_ticket_search,
)
from rest_framework.exceptions import NotFound

class TicketService:

    @staticmethod
    def search_tickets(validated_filters):
        cached_results = get_cached_ticket_search(
            validated_filters
        )
        if cached_results is not None:
            return {
                "results": cached_results,
                "cached": True,
            }
        results = TicketRepository.search_tickets(filters=validated_filters)
        cache_ticket_search(filters=validated_filters, results=results)
        return {
            "results": results,
            "cached": False,
        }

    @staticmethod
    def get_ticket_details(ticket_category_id):
        return TicketRepository.get_ticket_details(ticket_category_id=ticket_category_id)
