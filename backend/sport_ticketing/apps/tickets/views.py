from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response
from apps.tickets.serializers import (
    TicketSearchQuerySerializer,
    TicketSearchResultSerializer,
    TicketDetailSerializer,
    UserBookingSerializer,
    CancellationInfoSerializer,
    CancelTicketResponseSerializer,
    AdvancedTicketSearchQuerySerializer,
)
from apps.tickets.services import TicketService
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from apps.accounts.authentication import (
    JWTAuthentication,
)



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
def advanced_search_tickets(request):
    query_serializer = AdvancedTicketSearchQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": (
                    query_serializer.errors
                ),
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )
    result = (
        TicketService
        .advanced_search_tickets(
            validated_filters=(
                query_serializer
                .validated_data
            )
        )
    )
    response_serializer = (
        TicketSearchResultSerializer(
            result["results"],
            many=True,
        )
    )
    return Response(
        {
            "success": True,
            "message": (
                "Advanced ticket search "
                "completed successfully."
            ),
            "data": {
                "tickets": (
                    response_serializer.data
                ),
                "count": len(
                    response_serializer.data
                ),
                "total": result["total"],
                "limit": (
                    query_serializer
                    .validated_data[
                        "limit"
                    ]
                ),
                "offset": (
                    query_serializer
                    .validated_data[
                        "offset"
                    ]
                ),
                "engine": (
                    "elasticsearch"
                ),
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


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = TicketService.get_user_bookings(user_id=request.user.id)
    upcoming_serializer = UserBookingSerializer(bookings["upcoming"], many=True)
    cancelled_serializer = UserBookingSerializer(bookings["cancelled"], many=True)
    used_serializer = UserBookingSerializer(bookings["used"], many=True)
    past_serializer = UserBookingSerializer(bookings["past"], many=True)
    return Response(
        {
            "success": True,
            "message": (
                "User bookings retrieved successfully."
            ),
            "data": {
                "upcoming": upcoming_serializer.data,
                "cancelled": cancelled_serializer.data,
                "used": used_serializer.data,
                "past": past_serializer.data,

                "counts": {
                    "upcoming": len(
                        upcoming_serializer.data
                    ),
                    "cancelled": len(
                        cancelled_serializer.data
                    ),
                    "used": len(
                        used_serializer.data
                    ),
                    "past": len(
                        past_serializer.data
                    ),
                },
                "total_count": (
                    len(upcoming_serializer.data)
                    + len(cancelled_serializer.data)
                    + len(used_serializer.data)
                    + len(past_serializer.data)
                ),
            },
        },
        status=status.HTTP_200_OK,
    )



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancellation_info(request, ticket_id):
    result = TicketService.get_cancellation_info(ticket_id=ticket_id, user_id=request.user.id)
    response_serializer = CancellationInfoSerializer(result)
    return Response(
        {
            "success": True,
            "message": (
                "Cancellation information "
                "retrieved successfully."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_ticket(request, ticket_id):
    result = TicketService.cancel_user_ticket(ticket_id=ticket_id, user_id=request.user.id)
    response_serializer = CancelTicketResponseSerializer(result)
    return Response(
        {
            "success": True,
            "message": (
                "Ticket cancelled and refund "
                "processed successfully."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )