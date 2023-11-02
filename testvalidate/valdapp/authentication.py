from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone


class TokenAuthentication(BaseTokenAuth):
    keyword ="Bearer"
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key = key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")      
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")
        if token:
            tokencreated_time = token.created
            print(tokencreated_time)
            print(timezone.now(),"sdrdtdht")
            print(timezone.now()-tokencreated_time,"checking")
            compare = timezone.now()-tokencreated_time

            if compare > timedelta(hours = 1):
                token.delete()
                print("TOKEN IS deleted")
                raise AuthenticationFailed("The Token is expired")
        return (token.user, token) 


