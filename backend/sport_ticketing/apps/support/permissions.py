from rest_framework.permissions import (
    BasePermission,
)


class IsSupport(BasePermission):
    message = (
        "Only support users can access "
        "this endpoint."
    )

    def has_permission(self, request, view):
        user = request.user
        return (
            user is not None
            and getattr(user, "is_authenticated", False)
            and getattr(user, "role", None) == "support"
        )