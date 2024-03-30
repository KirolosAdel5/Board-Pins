import requests
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from urllib.parse import urlencode
from rest_framework_simplejwt.tokens import RefreshToken
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from random import SystemRandom

class GoogleRawLoginFlowService:
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(self):
        self.client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
        self.client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def get_authorization_url(self):
        redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
        scopes = "email profile"
        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scopes,
            "state": state,
            
        }
        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"
    
        return authorization_url, state

    def get_access_token(self, code, redirect_uri):
        params = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.GOOGLE_TOKEN_URL, data=params)
        return response.json()

    def get_user_info(self, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.GOOGLE_USERINFO_URL, headers=headers)
        return response.json()

    def get_access_and_refresh_tokens(self, user):
        serializer = TokenObtainPairSerializer()
        token_data = serializer.get_token(user)
        access_token = token_data.access_token
        refresh_token = RefreshToken.for_user(user)
        return access_token, refresh_token