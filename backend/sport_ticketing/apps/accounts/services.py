from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.accounts.otp import create_signup_otp, verify_signup_otp
from apps.accounts.repositories import UserRepository
from apps.accounts.tokens import generate_access_token


class AccountService:

    @staticmethod
    def request_signup_otp(validated_data):
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        if UserRepository.exists_by_email_or_phone(email=email, phone=phone):
            raise ValidationError({
                "detail": "A user with this email or phone already exists."
            })
        otp_data = create_signup_otp(email=email, phone=phone)
        return otp_data

    @staticmethod
    def register_user(validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        password = validated_data["password"]
        otp_code = validated_data["otp_code"]
        if UserRepository.exists_by_email_or_phone(email=email, phone=phone):
            raise ValidationError({
                "detail": "A user with this email or phone already exists."
            })
        is_valid_otp, verified_target_type = verify_signup_otp(
            email=email,
            phone=phone,
            otp_code=otp_code,
        )
        if not is_valid_otp:
            raise ValidationError({
                "otp_code": "Invalid or expired OTP code."
            })
        email_verified = verified_target_type == "email"
        phone_verified = verified_target_type == "phone"
        password_hash = make_password(password)
        with transaction.atomic():
            user = UserRepository.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password_hash=password_hash,
                role="customer",
                email_verified=email_verified,
                phone_verified=phone_verified,
            )
        access_token = generate_access_token(user)
        return {
            "user": user,
            "access_token": access_token,
        }