__all__ = ['create_slot']
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from calendar_format.calendar_view import get_crendentials
from datetime import timedelta
import datefinder

colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}


avail_times = ['2023-02-10 08:30:00']


credentials = get_crendentials(".cctoken.json")
credential = Credentials.from_authorized_user_info(info=credentials)
service = build('calendar', 'v3', credentials=credential)

import datefinder

def slot(avail_times):
    '''
    Asks volunteer what time they would like to make a slot.
    Checks valid date, time and weekdays.
    Check if slot is taken. !!!list for now, check times in database!!!
    '''
    while True:
        time_slot = input('What date and time would you like to book? i.e. 10 feb 2023 8:00: \n').lower()
        if time_slot == 'cancel':
            return ''

        matches = list(datefinder.find_dates(time_slot))
        if not matches:
            print(colors['RED'],'[>] You have entered an invalid date or time. You may enter cancel or...', colors['END'])
            continue

        start_time = matches[0]
        weekday = start_time.strftime('%A')
        hour = start_time.strftime('%H')
        minute = start_time.strftime('%M')

        if str(start_time) in avail_times:
            print(colors['BLUE'], '[>] The slot you have is not available. You may enter cancel or...', colors['END'])
            continue

        if weekday in ['Saturday', 'Sunday']:
            print(colors['MAGENTA'], '[>] The date you have entered is a weekend. You may enter cancel or...', colors['END'])
            continue

        if not(8 <= int(hour) <= 16) or minute not in ['00', '30']:
            print(colors['BLUE'], '''[>] The time you have entered is outside office hours or not half hourly.
You may enter cancel or...''', colors['END'])
            continue

        return time_slot


def create_slot(username, email, avail_times):
    '''
    Creates Volunteer slot on code clinic calendar and volunteer calendar.
    '''
    while True:
        time_slot = slot(avail_times)
        if not time_slot:
            return '', '', ''        
        break

            

    matches = list(datefinder.find_dates(time_slot))
    if matches:
        start_time = matches[0]
        end_time = start_time + timedelta(minutes=30)

    event_details = {
        'summary': username,
        'description': 'Volunteer available!',
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Africa/Johannesburg',
        },
        'creator': {
            'email': email,
            'self': False
        },
        'organizer': {
            'email': email,
            'self': True
        },
        'attendees': [
            {'email': email},
        ],
        'visibility': 'public',
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    maxAttendees = 3
    sendNotification = True
    sendUpdate = 'all'

    event = service.events().insert(
        calendarId='primary', body=event_details,
        maxAttendees=maxAttendees, sendNotifications=sendNotification,
        sendUpdates=sendUpdate).execute()

    eventId = event['id']
    eventSummary = event['summary']

    print(colors['GREEN'], '[>] You have successfully created a volunteer slot!', colors['END'])

    return eventId, eventSummary, str(start_time.strftime("%Y-%m-%dT%H:%M:%S"))


