from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from calendarWeedway.decorators import google_login_required

# Set to True to enable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def RedirectToLoginView(request):
    
    return HttpResponseRedirect(reverse('token_obtain_pair'))


class GoogleCalendarInitView(View):
    """
    Initiate the OAuth2 authorization flow.
    """

    def get(self, request, *args, **kwargs):
        # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
        )

        # Store the state so the callback can verify the auth server response.
        request.session['state'] = state

        # Redirect the user to the authorization URL.
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    """
    Callback view to handle the response from Google OAuth2 authorization server.

    This view is registered as the redirect_uri in the Google OAuth2 client
    configuration. The authorization server will redirect the user to this view
    after the user has granted or denied permission to the client.
    """

    def get(self, request, *args, **kwargs):
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = request.GET.get('state')

        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            state=state
        )
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials in the session.
        credentials = flow.credentials

        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        # Fetching of events is done in a separate view.
        # Here we just redirect to the events view.
        return redirect('http://localhost:8000/rest/v1/calendar/events/')


class GoogleCalendarEventsView(View):
    """
    Fetch events from Google Calendar.
    """
    @method_decorator(google_login_required)
    def get(self, request, *args, **kwargs):
        credentials = Credentials(
            **request.session['credentials']
        )

        service = build('calendar', 'v3', credentials=credentials)

        # Min time
        timeMin = '2022-01-01T00:00:00-07:00'

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=timeMin,
                                              maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return JsonResponse({'status': 'success',
                             'message': 'Events have been fetched.',
                             'data': events
                             })
    
class GoogleCalendarEventsCreate(View):
    @method_decorator(google_login_required)
    def get(self, request, *args, **kwargs):
        credentials = Credentials(
            **request.session['credentials']
        )

        service = build('calendar', 'v3', credentials=credentials)
        start_time = datetime(2023, 7, 26, 18, 30, 0)
        end_time = start_time + timedelta(hours=4)
        timezone = 'America/Sao_Paulo'

        event = {
            'summary': 'Evento Criado pela api da weedway',
            'location': 'Natal',
            'description': 'Primeiro evento criado',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        events_result = service.events().insert(calendarId='primary', body=event).execute()


        return JsonResponse({'status': 'success',
                             'message': 'Events have been fetched.',
                             'data': events_result
                             })