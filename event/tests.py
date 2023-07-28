from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from rest_framework import status
import os
from django.contrib.auth.models import User
from google_auth_oauthlib.flow import InstalledAppFlow

class CreateSerachScheduleTestCase(TestCase):
    def setUp(self):
        self.user_data={
            'email':'teste@teste.com',
            'password':'testeSenha',
            'first_name': 'teste', 
            'last_name': 'testando'
        }
        self.schedule_data={
            "user": 1,
            "date": "2023-07-28",
            "start_time": "17:00:00",
            "end_time": "19:00:00",
            "comments": "Comentario teste",
        }
        self.schedule_data_2={
            "user": 1,
            "date": "2023-07-29",
            "start_time": "17:00:00",
            "end_time": "19:00:00",
            "comments": "Comentario teste",
        }
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.login_url = '/api/token/'
        self.schedule_url = '/api/schedules-available/'

    def test_create_serach_schedule_available(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response_login = self.client.post(self.login_url, self.user_data, format='json')
        token = response_login.data['access']
        headers = {'Authorization': f'Bearer {token}'}

        response_create = self.client.post(self.schedule_url, self.schedule_data, headers=headers, format='json')
        self.client.post(self.schedule_url, self.schedule_data_2, headers=headers, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        response_get = self.client.get(self.schedule_url, headers=headers)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data["results"]), 2) 

        response_get_with_date_filter = self.client.get(self.schedule_url, {"date__gte": "2023-07-28", "date__lte": "2023-07-28", "start_time__gte": "12:00:00"}, headers=headers)
        self.assertEqual(response_get_with_date_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_with_date_filter.data["results"]), 1)

        response_retrieve = self.client.get(self.schedule_url+f'{1}/')
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_with_date_filter.data["results"]), 1)


#TODO: consegui fazer o test rodar e chegar na parte da autenticacao, porem ele pede pra acessar o link e se autenticar manualmente o que causa um erro
#      para verem ate onde consegui fazer 

# class CreateEventTestCase(TestCase):
#     def setUp(self):
#         self.event_data = {
#             "summary": "Sumaary teste",
#             "location": "Local teste",
#             "description": "Descricao teste",
#             "start": "2023-07-28T17:00:00.000-03:00",
#         }
#         self.client = Client()
#         self.redirect_url = reverse('calendar_redirect')
#         self.create_event_url = '/api/event/'
        
#         if 'credentials' not in self.client.session:
#             credentials_path = os.path.join(
#                 os.path.dirname(__file__),
#                 '..',                      
#                 'credentials.json'         
#             )
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 credentials_path,
#                 ['https://www.googleapis.com/auth/calendar.events']
#             )
#             creds = flow.run_local_server(port=0)
#             self.client.session['credentials'] = {
#                 'token': creds.token,
#                 'refresh_token': creds.refresh_token,
#                 'token_uri': creds.token_uri,
#                 'client_id': creds.client_id,
#                 'client_secret': creds.client_secret,
#                 'scopes': creds.scopes,
#             }


#     @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file')
#     def test_create_event_authenticated_with_google(self, mock_from_client_secrets_file):
#         mock_flow = MagicMock()
#         mock_flow.authorization_response = 'http://localhost/rest/v1/calendar/redirect/?code=mocked_code'
#         mock_flow.credentials.token = self.client.session['credentials']['token']
#         mock_flow.credentials.refresh_token = self.client.session['credentials']['refresh_token']
#         mock_flow.credentials.token_uri = self.client.session['credentials']['token_uri']
#         mock_flow.credentials.client_id = self.client.session['credentials']['client_id']
#         mock_flow.credentials.client_secret = self.client.session['credentials']['client_secret']
#         mock_flow.credentials.scopes = self.client.session['credentials']['scopes']
#         mock_from_client_secrets_file.return_value = mock_flow

#         response = self.client.get(self.redirect_url)
#         self.assertEqual(response.status_code, 302)

#         credentials = self.client.session['credentials']
#         self.assertIsInstance(credentials, dict)
#         print(credentials)
#         self.assertCountEqual(
#             ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes'],
#             credentials.keys()
#         )

#         response_create = self.client.post(self.create_event_url, self.event_data, format='json')
#         print(response_create.data)
#         self.assertEqual(response_create.status_code, status.HTTP_200_OK)
        
        





