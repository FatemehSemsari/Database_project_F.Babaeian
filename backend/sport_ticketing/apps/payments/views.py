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
from apps.payments.serializers import (
    PaymentRequestSerializer,
    PaymentResponseSerializer,
)
from apps.payments.services import (
    PaymentService,
)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pay_reservation(request):
    serializer = PaymentRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    payment = PaymentService.pay_reservation(user_id=request.user.id, validated_data=serializer.validated_data)
    response_serializer = PaymentResponseSerializer(payment)
    return Response(
        {
            "success": True,
            "message": (
                "Payment completed successfully "
                "and ticket issued."
            ),
            "data": response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )