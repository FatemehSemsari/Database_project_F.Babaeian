import jwt
from django.conf import settings
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.repositories import UserRepository


class AuthenticatedUser:
    def __init__(self, user_data):
        self.id = user_data["id"]
        self.role = user_data["role"]
        self.email = user_data.get("email")
        self.phone = user_data.get("phone")
        self.data = user_data
    @property
    def is_authenticated(self):
        return True

class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()
        if not auth_header:
            return None
        if auth_header[0].lower() != self.keyword.lower().encode():
            raise AuthenticationFailed(
                "Authorization header must start with Bearer."
            )
        if len(auth_header) != 2:
            raise AuthenticationFailed(
                "Invalid Authorization header."
            )
        try:
            token = auth_header[1].decode("utf-8")
        except UnicodeError:
            raise AuthenticationFailed("Invalid token format.")
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Access token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid access token.")
        if payload.get("type") != "access":
            raise AuthenticationFailed("Invalid token type.")
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed(
                "User id is missing from token."
            )
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise AuthenticationFailed("User not found.")
        if not user["is_active"]:
            raise AuthenticationFailed("User account is inactive.")
        if payload.get("role") != user["role"]:
            raise AuthenticationFailed(
                "Token role does not match user role."
            )
        return AuthenticatedUser(user), token


# After authentication, this information will be available:
# request.user.id
# request.user.role
# request.user.email
# request.user.phone