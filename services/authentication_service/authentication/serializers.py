from .models import User
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.response import Response
import re
from django.contrib.auth.password_validation import validate_password
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    confirm_password = serializers.CharField(write_only=True, required=True)
    accept_terms = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'email_verified', 'profile_picture', 'subscription_plan', 'accept_terms']
        extra_kwargs = {
            'password': {'write_only': True},
            
                        'first_name': {'required': True},
                        'email': {'required': True},
                        'last_name': {'required': True},
                        'username': {'read_only': True}
                        }

    def validate_email(self, value):
        # Check if email is already registered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")

        return value

    def validate_password(self, value):
        # Check for strong password
        if not re.search(r'\d', value) or not re.search('[A-Z]', value):
            raise serializers.ValidationError("Password should contain at least 1 number and 1 uppercase letter.")

        validate_password(value)
        return value

    def validate(self, data):
        # Check if passwords match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        # Check if terms are accepted
        if not data.get('accept_terms'):
            raise serializers.ValidationError("Terms and conditions must be accepted.")

        return data

    def create(self, validated_data):
        name = validated_data['first_name'] + " " + validated_data['last_name']
       
        base_username = re.sub(r'\s+', '_', name).lower()

        while True:
            random_number = random.randint(1000, 9999)
            unique_username = f"{base_username}_{random_number}"
            try:
                User.objects.get(username=unique_username)
            except User.DoesNotExist:
                name = unique_username
                break

        user = User.objects.create_user(
            username=name,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            accept_terms = validated_data['accept_terms'],
        )
        
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ('uuid','username','first_name','last_name' ,'email','profile_picture', 'subscription_plan','is_staff','is_superuser') 