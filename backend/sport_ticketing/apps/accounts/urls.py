from django.urls import path
from apps.accounts.views import register, request_signup_otp

urlpatterns = [
    path("signup/otp/request/", request_signup_otp, name="signup-otp-request"),
    path("signup/", register, name="account-signup"),
]