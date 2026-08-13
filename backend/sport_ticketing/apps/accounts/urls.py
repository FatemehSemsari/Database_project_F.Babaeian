from django.urls import path
from apps.accounts.views import register, request_signup_otp, request_login_otp, login, profile,request_contact_change_otp,confirm_contact_change, change_password

urlpatterns = [
    path("signup/otp/request/", request_signup_otp, name="signup-otp-request"),
    path("signup/", register, name="account-signup"),
    path("login/otp/request/", request_login_otp, name="login-otp-request"),
    path("login/", login, name="account-login"),
    path("profile/",profile,name="account-profile"),
    path("profile/contact-change/otp/request/",request_contact_change_otp,name="contact-change-otp-request"),
    path("profile/contact-change/confirm/",confirm_contact_change,name="contact-change-confirm"),
    path("profile/password/change/",change_password, name="account-password-change"),
]