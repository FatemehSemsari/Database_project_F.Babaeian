from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.accounts.otp import *
from apps.accounts.repositories import UserRepository
from apps.accounts.tokens import generate_access_token
from apps.accounts.serializers import detect_identifier_type
from django.contrib.auth.hashers import check_password


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

    @staticmethod
    def request_login_otp(validated_data):
        identifier = validated_data.get("identifier")
        password = validated_data.get("password")
        identifier_type, value = detect_identifier_type(identifier)
        email = None
        phone = None
        if identifier_type == "email":
            email = value
            user = UserRepository.get_user_by_email(email=email)
        else:
            phone = value
            user = UserRepository.get_user_by_phone(phone=phone)
        if not user:
            raise ValidationError({
                "detail": "You have not registered an account yet."
            })
        if not user["is_active"]:
            raise ValidationError({
                "detail": "Your account is inactive."
            })
        if phone and not user["phone_verified"]:
            raise ValidationError({
                "detail": "You have not verified your phone number. Try to login with email."
            })
        if email and not user["email_verified"]:
            raise ValidationError({
                "detail": "You have not verified your email address. Try to login with phone."
            })
        if not check_password(password, user["password_hash"]):
            raise ValidationError({
                "detail": "Password is incorrect."
            })
        otp_data = create_login_otp(email=email, phone=phone)
        return otp_data


    @staticmethod
    def login(validated_data):
        identifier = validated_data.get("identifier")
        otp_code = validated_data.get("otp_code")
        email = None
        phone = None
        identifier_type, identifier_value = detect_identifier_type(identifier)
        if identifier_type == "phone":
            phone = identifier_value
            user = UserRepository.get_user_by_phone(phone=phone)
        else:
            email = identifier_value
            user = UserRepository.get_user_by_email(email)
        if not user:
            raise ValidationError({
                "detail": "User not found."
            })
        is_valid_otp, verified_target_type = verify_login_otp(
            email=email,
            phone=phone,
            otp_code=otp_code,
        )
        if not is_valid_otp:
            raise ValidationError({
                "otp_code": "Invalid or expired OTP code."
            })
        access_token = generate_access_token(user)
        user.pop("password_hash", None)
        return {
            "user": user,
            "access_token": access_token,
        }

