from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password

class SignupOtpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_phone(self, value):
        if value in (None, ""):
            return None
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if not value.startswith("09"):
            raise serializers.ValidationError("Phone number must start with 09.")
        return value

    def validate_email(self, value):
        if value in (None, ""):
            return None
        return value.strip().lower()

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError("Email or phone is required.")
        return attrs


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    otp_code = serializers.CharField(write_only=True, min_length=6, max_length=6)

    def validate_phone(self, value):
        if value in (None, ""):
            return None
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if not value.startswith("09"):
            raise serializers.ValidationError("Phone number must start with 09.")
        return value

    def validate_email(self, value):
        if value in (None, ""):
            return None
        return value.strip().lower()

    def validate_otp_code(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError("Email or phone is required.")
        return attrs


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    role = serializers.CharField()
    email_verified = serializers.BooleanField()
    phone_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(required=False)

def detect_identifier_type(identifier):
    identifier = (identifier or "").strip().lower()
    if not identifier:
        raise serializers.ValidationError("Email or phone is required.")
    if identifier.isdigit() and len(identifier) == 11 and identifier.startswith("09"):
        return "phone", identifier
    try:
        validate_email(identifier)
        return "email", identifier
    except DjangoValidationError:
        raise serializers.ValidationError(
            "Identifier must be a valid email or phone number."
        )


class LoginOTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_identifier(self, value):
        _, normalized_identifier = detect_identifier_type(value)
        return normalized_identifier

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    otp_code = serializers.CharField(write_only=True, min_length=6, max_length=6)

    def validate_identifier(self, value):
        _, normalized_identifier = detect_identifier_type(value)
        return normalized_identifier

    def validate_otp_code(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value

    def validate(self, attrs):
        if not attrs.get("identifier"):
            raise serializers.ValidationError("Email or phone is required.")
        if not attrs.get("otp_code"):
            raise serializers.ValidationError("OTP code is required.")
        return attrs


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False,
        max_length=100,
        allow_blank=False,
        trim_whitespace=True,
    )
    last_name = serializers.CharField(
        required=False,
        max_length=100,
        allow_blank=False,
        trim_whitespace=True,
    )

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "First name cannot be empty."
            )
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Last name cannot be empty."
            )
        return value

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one profile field must be provided."
            )
        return attrs


class ContactChangeOTPRequestSerializer(serializers.Serializer):
    identifier_type = serializers.ChoiceField(choices=["email", "phone"])
    new_identifier = serializers.CharField(max_length=255,trim_whitespace=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        identifier_type = attrs["identifier_type"]
        new_identifier = attrs["new_identifier"]
        detected_type, normalized_identifier = detect_identifier_type(new_identifier)
        if detected_type != identifier_type:
            raise serializers.ValidationError({
                "new_identifier": (
                    f"The entered value is not a valid {identifier_type}."
                )
            })
        attrs["new_identifier"] = normalized_identifier
        return attrs

class ContactChangeConfirmSerializer(serializers.Serializer):
    identifier_type = serializers.ChoiceField(choices=["email", "phone"])
    new_identifier = serializers.CharField(max_length=255,trim_whitespace=True)
    otp_code = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=6,
        trim_whitespace=True)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP code must contain only digits."
            )
        return value

    def validate(self, attrs):
        identifier_type = attrs["identifier_type"]
        new_identifier = attrs["new_identifier"]
        detected_type, normalized_identifier = detect_identifier_type(
            new_identifier
        )
        if detected_type != identifier_type:
            raise serializers.ValidationError({
                "new_identifier": (
                    f"The entered value is not a valid {identifier_type}."
                )
            })
        attrs["new_identifier"] = normalized_identifier
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        trim_whitespace=False,
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        trim_whitespace=False,
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                "new_password_confirm": "New passwords do not match."
            })
        try:
            validate_password(new_password)
        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "new_password": list(error.messages)
            })
        return attrs