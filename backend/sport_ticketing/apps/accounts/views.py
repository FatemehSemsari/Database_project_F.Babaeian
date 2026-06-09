from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.accounts.serializers import (
    SignupOtpRequestSerializer,
    RegisterSerializer,
    UserResponseSerializer, LoginOTPRequestSerializer, LoginSerializer,
)
from apps.accounts.services import AccountService


@api_view(["POST"])
@permission_classes([AllowAny])
def request_signup_otp(request):
    serializer = SignupOtpRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    result = AccountService.request_signup_otp(serializer.validated_data)
    return Response(
        {
            "success": True,
            "message": f"OTP sent to {result['target_type']}.",
            "data": {
                "target_type": result["target_type"],
                "target_value": result["target_value"],
                "otp_code_for_test": result["otp_code"],
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    result = AccountService.register_user(serializer.validated_data)
    user_data = UserResponseSerializer(result["user"]).data
    return Response(
        {
            "success": True,
            "message": "User registered successfully.",
            "data": {
                "user": user_data,
                "access_token": result["access_token"],
            },
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def request_login_otp(request):
    serializer = LoginOTPRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    result = AccountService.request_login_otp(serializer.validated_data)
    return Response(
        {
            "success": True,
            "message": f"OTP sent to {result['target_type']}.",
            "data": {
                "target_type": result["target_type"],
                "target_value": result["target_value"],
                "otp_code_for_test": result["otp_code"],
            }
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    result = AccountService.login(serializer.validated_data)
    user_data = UserResponseSerializer(result["user"]).data
    return Response(
        {
            "success": True,
            "message": "User logged in successfully.",
            "data": {
                "user": user_data,
                "access_token": result["access_token"],
            }
        },
        status=status.HTTP_200_OK,
    )
