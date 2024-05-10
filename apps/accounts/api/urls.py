from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.accounts.api.views import (UserRegistrationView, LoginView,
                               PasswordResetRequestView, OTPVerificationView,
                               PasswordResetView, ChangePasswordView,
                               VerifyEmailView, GetMeApiView
                               )


urlpatterns = [
    path('token/', LoginView.as_view(), name='register'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('getme/', GetMeApiView.as_view(), name='get-me'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp_verification'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
