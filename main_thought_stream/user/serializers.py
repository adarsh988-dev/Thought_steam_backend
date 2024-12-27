from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        # Username cannot be empty
        if not value:
            raise serializers.ValidationError("Username cannot be empty.")
        
        # Username must consist of letters and numbers only
        if not re.match("^[a-zA-Z0-9]*$", value):
            raise serializers.ValidationError("Username must consist of letters and numbers only.")
        
        # Username length should be between 5 and 20 characters
        if len(value) < 5 or len(value) > 20:
            raise serializers.ValidationError("Username length must be between 5 and 20 characters.")
        
        # Username should not be a duplicate
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        
        return value

    def validate_password(self, value):
        # Password cannot be empty
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")
        
        # Password length should be between 8 and 20 characters
        if len(value) < 8 or len(value) > 20:
            raise serializers.ValidationError("Password length must be between 8 and 20 characters.")
        
        # Password should contain at least one uppercase letter, one lowercase letter, one number, and one special character
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):  # Check for special characters
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value

    def validate_email(self, value):
        # Email cannot be empty
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        
        # Check if email is in the correct format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")
        
        # Email should not be a duplicate
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        
        return value

    def create(self, validated_data):
        # Create the user using the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user

class UserLoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

        def validate(self, attrs):
            username = attrs.get('username')
            password = attrs.get('password')
            if not username or not password:
                raise serializers.ValidationError("Both username and password are required.")
            user = authenticate(username = username, password = password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            attrs['user'] = user
            return attrs

