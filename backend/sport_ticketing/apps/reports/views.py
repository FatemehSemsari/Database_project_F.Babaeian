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
from apps.reports.serializers import (
    CreateReportSerializer,
    ReportResponseSerializer,
    UserReportSerializer
)
from apps.reports.services import (
    ReportService,
)


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_report(request):
    # GET - LIST CURRENT USER REPORTS
    if request.method == "GET":
        reports = (
            ReportService
            .get_user_reports(
                user_id=request.user.id
            )
        )
        response_serializer = (
            UserReportSerializer(
                reports,
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


    # POST - CREATE REPORT
    serializer = CreateReportSerializer(
        data=request.data
    )
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    report = ReportService.create_report(
        user_id=request.user.id,
        validated_data=(
            serializer.validated_data
        ),
    )
    response_serializer = (
        ReportResponseSerializer(
            report
        )
    )
    return Response(
        {
            "success": True,
            "message": (
                "Report submitted successfully."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )
