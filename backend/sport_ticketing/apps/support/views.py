from rest_framework import status

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.response import Response

from apps.accounts.authentication import (
    JWTAuthentication,
)

from apps.support.permissions import (
    IsSupport,
)

from apps.support.serializers import (
    PaginationQuerySerializer,
    ReportListQuerySerializer,
    ReservationListQuerySerializer,

    CancelledTicketSerializer,
    SuspiciousPaymentSerializer,

    SupportReportSerializer,
    UpdateReportSerializer,

    SupportReservationSerializer,
    UpdateReservationSerializer,
    ReservationActionResponseSerializer,
)

from apps.support.services import (
    SupportService,
)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def cancelled_tickets(request):

    serializer = PaginationQuerySerializer(
        data=request.query_params
    )

    serializer.is_valid(
        raise_exception=True
    )

    results = (
        SupportService
        .get_cancelled_tickets(
            serializer.validated_data
        )
    )

    response_serializer = (
        CancelledTicketSerializer(
            results,
            many=True,
        )
    )

    return Response(
        {
            "success": True,
            "data": {
                "tickets": (
                    response_serializer.data
                ),
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def suspicious_payments(request):

    serializer = PaginationQuerySerializer(
        data=request.query_params
    )

    serializer.is_valid(
        raise_exception=True
    )

    results = (
        SupportService
        .get_suspicious_payments(
            serializer.validated_data
        )
    )

    response_serializer = (
        SuspiciousPaymentSerializer(
            results,
            many=True,
        )
    )

    return Response(
        {
            "success": True,
            "data": {
                "payments": (
                    response_serializer.data
                ),
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def reports(request):

    serializer = ReportListQuerySerializer(
        data=request.query_params
    )

    serializer.is_valid(
        raise_exception=True
    )

    results = SupportService.get_reports(
        serializer.validated_data
    )

    response_serializer = (
        SupportReportSerializer(
            results,
            many=True,
        )
    )

    return Response(
        {
            "success": True,
            "data": {
                "reports": (
                    response_serializer.data
                ),
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def update_report(
    request,
    report_id,
):
    serializer = UpdateReportSerializer(
        data=request.data,
        partial=True,
    )

    serializer.is_valid(
        raise_exception=True
    )

    result = SupportService.update_report(
        report_id=report_id,

        support_user_id=(
            request.user.id
        ),

        validated_data=(
            serializer.validated_data
        ),
    )

    response_serializer = (
        SupportReportSerializer(
            result
        )
    )

    return Response(
        {
            "success": True,
            "message": (
                "Report reviewed successfully."
            ),
            "data": (
                response_serializer.data
            ),
        },
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def reservations(request):

    serializer = (
        ReservationListQuerySerializer(
            data=request.query_params
        )
    )

    serializer.is_valid(
        raise_exception=True
    )

    results = (
        SupportService.get_reservations(
            serializer.validated_data
        )
    )

    response_serializer = (
        SupportReservationSerializer(
            results,
            many=True,
        )
    )

    return Response(
        {
            "success": True,
            "data": {
                "reservations": (
                    response_serializer.data
                ),
                "count": len(
                    response_serializer.data
                ),
            },
        },
        status=status.HTTP_200_OK,
    )

@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([
    IsAuthenticated,
    IsSupport,
])
def update_reservation(
    request,
    reservation_id,
):
    serializer = (
        UpdateReservationSerializer(
            data=request.data
        )
    )

    serializer.is_valid(
        raise_exception=True
    )

    result = (
        SupportService
        .update_reservation(
            reservation_id=(
                reservation_id
            ),

            support_user_id=(
                request.user.id
            ),

            validated_data=(
                serializer.validated_data
            ),
        )
    )

    response_serializer = (
        ReservationActionResponseSerializer(
            result
        )
    )

    return Response(
        {
            "success": True,
            "message": (
                "Reservation updated "
                "successfully."
            ),
            "data": (
                response_serializer.data
            ),
        },
        status=status.HTTP_200_OK,
    )
