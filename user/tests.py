from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.user_data={
            'email':'teste@teste.com',
            'password':'testeSenha',
            'first_name': 'teste', 
            'last_name': 'testando'
        }
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.login_url = '/api/token/'
        self.user_list_url = '/api/users/'

    def test_create_login_user_acess_authenticated_url(self):
        response_create = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        response_login = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_login.data)

        token = response_login.data['access']

        headers = {'Authorization': f'Bearer {token}'}

        response_profile = self.client.get(self.user_list_url, headers=headers)
        self.assertEqual(response_profile.status_code, status.HTTP_200_OK)


class GoogleCalendarAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.init_url = reverse('calendar_init')
        self.redirect_url = reverse('calendar_redirect')
        self.events_url = reverse('calendar_events')

    def test_google_calendar_init_view(self):
        response = self.client.get(self.init_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://accounts.google.com', response.url)

    @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file')
    def test_google_calendar_redirect_view(self, mock_from_client_secrets_file):

        mock_flow = MagicMock()
        mock_flow.authorization_response = 'http://localhost/rest/v1/calendar/redirect/?code=mocked_code'
        mock_flow.credentials.token = 'mocked_token'
        mock_flow.credentials.refresh_token = 'mocked_refresh_token'
        mock_flow.credentials.token_uri = 'https://oauth2.googleapis.com/token'
        mock_flow.credentials.client_id = 'mocked_client_id'
        mock_flow.credentials.client_secret = 'mocked_client_secret'
        mock_flow.credentials.scopes = ['https://www.googleapis.com/auth/calendar.events']
        mock_from_client_secrets_file.return_value = mock_flow

        response = self.client.get(self.redirect_url)
        self.assertEqual(response.status_code, 302)

        credentials = self.client.session['credentials']
        self.assertIsInstance(credentials, dict)
        self.assertCountEqual(
            ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes'],
            credentials.keys()
        )


