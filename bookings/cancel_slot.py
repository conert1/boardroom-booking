__all__ = ['cancel_slot']
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


def check_slot(username, eventId):
    '''
    Checks if volunteer can cancel slot.
    Checks if & is in eventSummary.
    '''
    try:
        event = service.events().get(
            calendarId='primary', eventId=eventId).execute()

        eventSummary = event['summary']
        if '&' not in eventSummary and username == eventSummary:
            return True
    except:
        return False


def cancel_slot(username, eventId):

    if check_slot(username, eventId):
        sendNotification = True
        sendUpdate = 'all'
        service.events().delete(calendarId='primary', eventId=eventId,
                                sendNotifications=sendNotification, 
                                sendUpdates=sendUpdate).execute()

        print(colors['YELLOW'], '[>] You have successfully cancelled your volunteer slot.', colors['END'])
        return True
    else:
        print(colors['BLUE'], '''[>] You can not cancel your slot because a student has already booked it,
or the slot belongs to another volunteer.''', colors['END'])




