from django.contrib.auth.hashers import (
    make_password,
    check_password,
)
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError, NotFound, Throttled

from apps.accounts.otp import (
    create_signup_otp,
    verify_signup_otp,
    delete_signup_otp,
    create_login_otp,
    verify_login_otp,
    create_contact_change_otp,
    verify_contact_change_otp,
    delete_contact_change_otp,
)
from apps.accounts.repositories import UserRepository
from apps.accounts.tokens import generate_access_token
from apps.accounts.serializers import detect_identifier_type
from apps.accounts.profile_cache import (
    get_cached_profile,
    cache_profile,
    delete_cached_profile,
)



def ensure_otp_was_created(otp_data):
    if not otp_data["created"]:
        raise Throttled(
            wait=otp_data["retry_after"],
            detail=(
                "Please wait before requesting another OTP."
            ),
        )
    otp_data.pop("created", None)
    otp_data.pop("retry_after", None)
    return otp_data


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
        return ensure_otp_was_created(otp_data)


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
        delete_signup_otp(email=email, phone=phone)
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
        return ensure_otp_was_created(otp_data)


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


    @staticmethod
    def get_profile(user_id):
        cached_profile = get_cached_profile(user_id)
        if cached_profile:
            return cached_profile
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise NotFound("User profile not found.")
        if not user["is_active"]:
            raise ValidationError({
                "detail": "User account is inactive."
            })
        cache_profile(user)
        return user


    @staticmethod
    def update_profile(user_id, validated_data):
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        with transaction.atomic():
            updated_user = UserRepository.update_profile(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
            )
        if not updated_user:
            raise NotFound("User profile not found.")
        delete_cached_profile(user_id)
        cache_profile(updated_user)
        return updated_user


    @staticmethod
    def request_contact_change_otp(user_id, validated_data):
        identifier_type = validated_data["identifier_type"]
        new_identifier = validated_data["new_identifier"]
        password = validated_data["password"]
        user = UserRepository.get_user_auth_by_id(user_id)
        if not user:
            raise NotFound("User not found.")
        if not user["is_active"]:
            raise ValidationError({
                "detail": "Your account is inactive."
            })
        if not check_password(password, user["password_hash"]):
            raise ValidationError({
                "password": "Current password is incorrect."
            })
        if identifier_type == "email":
            if user.get("email") == new_identifier:
                raise ValidationError({
                    "new_identifier": (
                        "This email is already registered on your account."
                    )
                })
            email = new_identifier
            phone = None
        else:
            if user.get("phone") == new_identifier:
                raise ValidationError({
                    "new_identifier": (
                        "This phone number is already registered on your account."
                    )
                })
            email = None
            phone = new_identifier
        if UserRepository.exists_by_email_or_phone(email=email,phone=phone):
            raise ValidationError({
                "new_identifier": (
                    "Another user is already using this email or phone."
                )
            })
        otp_data = create_contact_change_otp(
            user_id=user_id,
            identifier_type=identifier_type,
            new_identifier=new_identifier,
        )

        return ensure_otp_was_created(otp_data)

    @staticmethod
    def confirm_contact_change(user_id, validated_data):
        identifier_type = validated_data["identifier_type"]
        new_identifier = validated_data["new_identifier"]
        otp_code = validated_data["otp_code"]
        user = UserRepository.get_user_auth_by_id(user_id)
        if not user:
            raise NotFound("User not found.")
        if not user["is_active"]:
            raise ValidationError({
                "detail": "Your account is inactive."
            })
        is_valid_otp = verify_contact_change_otp(
            user_id=user_id,
            identifier_type=identifier_type,
            new_identifier=new_identifier,
            otp_code=otp_code,
        )
        if not is_valid_otp:
            raise ValidationError({
                "otp_code": "Invalid or expired OTP code."
            })
        if identifier_type == "email":
            if user.get("email") == new_identifier:
                raise ValidationError({
                    "new_identifier": (
                        "This email is already registered on your account."
                    )
                })
            email = new_identifier
            phone = None
        else:
            if user.get("phone") == new_identifier:
                raise ValidationError({
                    "new_identifier": (
                        "This phone number is already registered on your account."
                    )
                })
            email = None
            phone = new_identifier
        if UserRepository.exists_by_email_or_phone(
                email=email,
                phone=phone,
        ):
            raise ValidationError({
                "new_identifier": (
                    "Another user is already using this email or phone."
                )
            })
        try:
            with transaction.atomic():
                if identifier_type == "email":
                    updated_user = UserRepository.update_email(
                        user_id=user_id,
                        new_email=new_identifier,
                    )
                else:
                    updated_user = UserRepository.update_phone(
                        user_id=user_id,
                        new_phone=new_identifier,
                    )
        except IntegrityError:
            raise ValidationError({
                "new_identifier": (
                    "Another user is already using this email or phone."
                )
            })
        if not updated_user:
            raise NotFound("User not found.")
        delete_contact_change_otp(user_id=user_id,identifier_type=identifier_type)
        delete_cached_profile(user_id)
        cache_profile(updated_user)
        return updated_user

    @staticmethod
    def change_password(user_id, validated_data):
        current_password = validated_data["current_password"]
        new_password = validated_data["new_password"]
        user = UserRepository.get_user_auth_by_id(user_id)
        if not user:
            raise NotFound("User not found.")
        if not user["is_active"]:
            raise ValidationError({
                "detail": "Your account is inactive."
            })
        if not check_password(current_password, user["password_hash"]):
            raise ValidationError({
                "current_password": "Current password is incorrect."
            })
        if check_password(new_password, user["password_hash"]):
            raise ValidationError({
                "new_password": (
                    "New password must be different from current password."
                )
            })
        new_password_hash = make_password(new_password)
        with transaction.atomic():
            password_updated = UserRepository.update_password(user_id=user_id, new_password_hash=new_password_hash)
        if not password_updated:
            raise NotFound("User not found.")
        return {
            "password_changed": True,
        }