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
)
from apps.reports.services import (
    ReportService,
)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_report(request):
    serializer = CreateReportSerializer(data=request.data)
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
    response_serializer = ReportResponseSerializer(report)
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
