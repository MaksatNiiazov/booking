from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import UserAccount


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = UserAccount.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password')

        # if not user.email_verified:
        #     raise serializers.ValidationError('Email not verified. Please verify your email before logging in.')
        
        attrs['user'] = user
        return attrs
    

class PasswordResetRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = UserAccount.objects.get(email=value)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = UserAccount.objects.get(email=email)
            if user.otp != otp:
                raise serializers.ValidationError("Invalid OTP.")
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        try:
            user = UserAccount.objects.get(email=value)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.otp = None  
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')

        if current_password == new_password:
            raise serializers.ValidationError('New password cannot be the same as the current password')

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=64, write_only=True)

    def validate(self, data):
        email = data.get('email')
        verification_code = data.get('verification_code')

        try:
            user = UserAccount.objects.get(email=email)
            if user.verification_code != verification_code:
                raise serializers.ValidationError("Invalid verification code.")
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        refresh = super().get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = (
            "last_login",
            "date_joined",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
