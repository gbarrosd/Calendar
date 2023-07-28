from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from event.models import ScheduleAvailable
from django.utils import timezone as zone

def create_event(request, pk_schedule=None):
    try:
        data = request.data
        credentials = Credentials(
            **request.session['credentials']
        )
        service = build('calendar', 'v3', credentials=credentials)
        if pk_schedule:

            schedule = ScheduleAvailable.objects.get(pk=pk_schedule)
            if schedule.occupy == True:
                return "Vaga já ocupada"

            start_time = datetime.combine(schedule.date, schedule.start_time)
            end_time = datetime.combine(schedule.date, schedule.end_time)
            tzinfo = zone.get_current_timezone()
            timezone = str(tzinfo)

            event = {
                'summary': data.get("summary") or None,
                'location': data.get("location") or None,
                'description': data.get("description") or None,
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
            schedule.occupy = True
            schedule.save()

        else:
            start_time = datetime.strptime(data.get("start"), "%Y-%m-%dT%H:%M:%S.%f%z")
            duration = data.get("duration") or 1
            end_time = start_time + timedelta(hours=duration)
            tzinfo = zone.get_current_timezone()
            timezone = str(tzinfo)

            event = {
                'summary': data.get("summary") or None,
                'location': data.get("location") or None,
                'description': data.get("description") or None,
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

        return events_result

    except Exception as e:
        error_message = str(e)
        return {"Erro": error_message}