import random

from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.accounts.api.serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    PasswordResetRequestEmailSerializer,
    OTPVerificationSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer,
    MyTokenObtainPairSerializer,
    VerifyEmailSerializer,
    UserGetSerializer,
)

from apps.accounts.models import UserAccount
from apps.accounts.sender import send_verification_email
from apps.company.models import Company


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)

            response_data = {
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "message": "User registered successfully. Please check your email to verify your account."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print('da')
            refresh = MyTokenObtainPairSerializer().get_token(user=user)
            print('qwe')
            response_data = {
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message': 'Login successful.',
                'tokens': refresh
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserAccount.objects.get(email=email)

            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is: {otp}",
                from_email="your_email@example.com",
                recipient_list=[email],
            )

            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified. You can now reset your password."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = UserAccount.objects.get(email=serializer.validated_data['email'])
            serializer.update(user, serializer.validated_data)

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        email = request.GET.get('email')
        code = request.GET.get('code')
        
        try:
            user = UserAccount.objects.get(email=email)
            
            if user.verification_code == code:
                user.email_verified = True
                user.verification_code = None  
                user.save()
                
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
            
        except UserAccount.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class GetMeApiView(generics.GenericAPIView):
    """Позволяет пользователю получить информацию о себе"""
    serializer_class = UserGetSerializer

    def get(self, request):
        user = self.request.user

        return Response(
            {
                "user": UserGetSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
