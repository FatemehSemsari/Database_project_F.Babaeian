from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.tickets.serializers import (
    TicketSearchQuerySerializer,
    TicketSearchResultSerializer,
    TicketDetailSerializer,
)
from apps.tickets.services import TicketService


@api_view(["GET"])
@permission_classes([AllowAny])
def search_tickets(request):
    query_serializer = TicketSearchQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    result = TicketService.search_tickets(
        validated_filters=(
            query_serializer.validated_data
        )
    )
    response_serializer = TicketSearchResultSerializer(
        result["results"],
        many=True,
    )
    return Response(
        {
            "success": True,
            "message": (
                "Available tickets retrieved successfully."
            ),
            "data": {
                "tickets": response_serializer.data,
                "count": len(response_serializer.data),
                "limit": (
                    query_serializer.validated_data[
                        "limit"
                    ]
                ),
                "offset": (
                    query_serializer.validated_data[
                        "offset"
                    ]
                ),
                "cached": result["cached"],
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def ticket_details(request, ticket_category_id):
    ticket = TicketService.get_ticket_details(ticket_category_id=ticket_category_id)
    if ticket is None:
        return Response(
            {
                "success": False,
                "message": "Ticket category not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    response_serializer = TicketDetailSerializer(ticket)
    return Response(
        {
            "success": True,
            "message": (
                "Ticket details retrieved successfully."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )