from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    print("refresh tokens :", refresh)
    access_token = str(refresh.access_token)
    return {
        'access_token': access_token,
        'refresh_token': str(refresh)   
    }

class RegisterView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication] 
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            response = serializer.save()
            print("User created:", response)
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication] 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print("User logged in:", user)
            response = get_token_for_user(user)
            response['username'] = serializer.validated_data['username']
            response['email'] = user.email
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

