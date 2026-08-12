from rest_framework import status
from rest_framework.response import Response
from apps.accounts.authentication import JWTAuthentication
from apps.accounts.serializers import (
    SignupOtpRequestSerializer,
    RegisterSerializer,
    UserResponseSerializer,
    LoginOTPRequestSerializer,
    LoginSerializer,
    UserProfileUpdateSerializer,
    ContactChangeOTPRequestSerializer,
    ContactChangeConfirmSerializer,
    ChangePasswordSerializer,
)
from apps.accounts.services import AccountService
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.accounts.authentication import JWTAuthentication



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

@api_view(["GET", "PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        user = AccountService.get_profile(
            user_id=request.user.id
        )
        user_data = UserResponseSerializer(user).data
        return Response(
            {
                "success": True,
                "message": "User profile retrieved successfully.",
                "data": {
                    "user": user_data,
                },
            },
            status=status.HTTP_200_OK,
        )
    serializer = UserProfileUpdateSerializer(
        data=request.data,
        partial=True,
    )
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    updated_user = AccountService.update_profile(
        user_id=request.user.id,
        validated_data=serializer.validated_data,
    )
    user_data = UserResponseSerializer(updated_user).data
    return Response(
        {
            "success": True,
            "message": "User profile updated successfully.",
            "data": {
                "user": user_data,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def request_contact_change_otp(request):
    serializer = ContactChangeOTPRequestSerializer(
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
    result = AccountService.request_contact_change_otp(
        user_id=request.user.id,
        validated_data=serializer.validated_data,
    )
    return Response(
        {
            "success": True,
            "message": (
                f"OTP sent to the new {result['target_type']}."
            ),
            "data": {
                "target_type": result["target_type"],
                "target_value": result["target_value"],
                "otp_code_for_test": result["otp_code"],
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def confirm_contact_change(request):
    serializer = ContactChangeConfirmSerializer(
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
    updated_user = AccountService.confirm_contact_change(
        user_id=request.user.id,
        validated_data=serializer.validated_data,
    )
    user_data = UserResponseSerializer(updated_user).data
    identifier_type = serializer.validated_data[
        "identifier_type"
    ]
    return Response(
        {
            "success": True,
            "message": (
                f"User {identifier_type} changed successfully."
            ),
            "data": {
                "user": user_data,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    AccountService.change_password(user_id=request.user.id, validated_data=serializer.validated_data)
    return Response(
        {
            "success": True,
            "message": "Password changed successfully.",
            "data": None,
        },
        status=status.HTTP_200_OK,
    )