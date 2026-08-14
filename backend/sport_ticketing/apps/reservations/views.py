from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.reservations.serializers import (
    AvailableSeatSerializer,
    AvailableSeatsQuerySerializer,
)
from apps.reservations.services import (
    ReservationService,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.decorators import (
    authentication_classes,
)
from apps.accounts.authentication import (
    JWTAuthentication,
)
from apps.reservations.serializers import (
    CreateReservationSerializer,
    ReservationResponseSerializer,
    UserReservationSerializer
)


@api_view(["GET"])
@permission_classes([AllowAny])
def available_seats(request):
    query_serializer = AvailableSeatsQuerySerializer(data=request.query_params)
    if not query_serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": query_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    ticket_category_id = (
        query_serializer.validated_data[
            "ticket_category_id"
        ]
    )
    seats = ReservationService.get_available_seats(ticket_category_id=ticket_category_id)
    response_serializer = AvailableSeatSerializer(seats, many=True)
    return Response(
        {
            "success": True,
            "message": (
                "Available seats retrieved successfully."
            ),
            "data": {
                "ticket_category_id": ticket_category_id,
                "seats": response_serializer.data,
                "count": len(response_serializer.data),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    serializer = CreateReservationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    reservation = (
        ReservationService.create_reservation(
            user_id=request.user.id,
            validated_data=(
                serializer.validated_data
            ),
        )
    )
    response_serializer = ReservationResponseSerializer(reservation)
    return Response(
        {
            "success": True,
            "message": (
                "Ticket reserved successfully."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_reservations(request):
    result = ReservationService.get_my_reservations(user_id=request.user.id)
    active_serializer = UserReservationSerializer(result["active"], many=True)
    history_serializer = UserReservationSerializer(result["history"], many=True)
    return Response(
        {
            "success": True,
            "message": (
                "Reservations retrieved successfully."
            ),
            "data": {
                "active": active_serializer.data,
                "active_count": len(
                    active_serializer.data
                ),
                "history": history_serializer.data,
                "history_count": len(
                    history_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )