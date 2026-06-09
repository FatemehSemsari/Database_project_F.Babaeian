from rest_framework import serializers


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