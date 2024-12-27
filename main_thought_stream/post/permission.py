from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User  # Assuming you're using the default User model

class CustomJWTAuthentication(BaseAuthentication):
    Bearer_Prefix = 'Bearer'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('No authorization header found')
        
        prefix, token = auth_header.split(' ')
        if prefix.lower() != self.Bearer_Prefix.lower():
            raise AuthenticationFailed('Authorization header must be Bearer token')

        try:
            access_token = AccessToken(token)
        except TokenError as e:
            raise AuthenticationFailed(f'Invalid token or token has expired: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'An error occurred while processing the token: {str(e)}')

    
        user_id = access_token.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('Token does not contain a valid user ID.')

        try:
           
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        request.user = user
        
        return (user, None) 
