from django.urls import path
from apps.accounts.views import register, request_signup_otp, request_login_otp, login

urlpatterns = [
    path("signup/otp/request/", request_signup_otp, name="signup-otp-request"),
    path("signup/", register, name="account-signup"),
    path("login/otp/request/", request_login_otp, name="login-otp-request"),
    path("login/", login, name="account-login"),
]