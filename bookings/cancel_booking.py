__all__ =  ['cancel_booking']
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from calendar_format.calendar_view import get_crendentials

credentials = get_crendentials(".cctoken.json")
credential = Credentials.from_authorized_user_info(info=credentials)
service = build('calendar', 'v3', credentials=credential)

colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}

def cancel_booking(username, eventId):
    '''
    Updates booked slot using eventId and removes as attendee.
    Removes username to summary and changes description.
    '''
    event = service.events().get(
        calendarId='primary', eventId=eventId).execute()

    if username in event['summary'].split(' & ')[1]:

        event['summary'] = event['summary'].split(' &')[0]
        event['description'] = 'Available to volunteer'
        event['attendees'] = [{'email': f"{event['summary']}@student.wethinkcode.co.za"}]

        sendNotification = True
        sendUpdate = 'all'

        updated_event = service.events().update(
            calendarId='primary', eventId=event['id'], body=event,
            sendNotifications=sendNotification, sendUpdates=sendUpdate
            ).execute()

        eventId = updated_event['id']
        eventSummary = updated_event['summary']

        print(colors['BLUE'], '[>] You have successfully cancelled your booking!', colors['END'])
        return eventId, eventSummary
    else:
        print(colors['MAGENTA'], "You can not cancel another student's booking.", colors['END'])
        return eventId, ''

