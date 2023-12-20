__all__ = ['make_booking']
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from collections import namedtuple
from calendar_format.calendar_view import get_crendentials
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


credentials = get_crendentials(".cctoken.json")
credential = Credentials.from_authorized_user_info(info=credentials)
service = build('calendar', 'v3', credentials=credential)

avail_times = ['2023-02-10 08:30:00']

def slot(avail_times):
    '''
    Asks volunteer what time they would like to make a slot.
    Only checking valid date and weekdays.
    Check if slot is available. !!!list for now, check times in database!!!
    '''
    while True:
        time_slot = input('What date and time would you like to book? i.e. 10 feb 2023 8:00: \n')
        if time_slot == 'cancel':
            return ''

        matches = list(datefinder.find_dates(time_slot))
        if matches:
            start_time = matches[0]
            
            for time in avail_times:
                avail = str(start_time.strftime("%Y-%m-%dT%H:%M:%S")) + "+02:00"

                if avail == time[1]:
                    return time[0], time[1]
                else:    
                    print(colors['RED'],'[>] There is no slot available at that time. You may enter cancel or...', colors['END'])

        else: 
            print(colors['RED'],'[>]You have entered an invalid date or time. You may enter cancel or...')
            
        return


def description():
    '''
    Asks student what they would like assistance with.
    Uses this as the event description.
    '''
    while True:
        descript = input('What would you like help with? \n')
        if not descript:
            continue
        else:
            return descript

Booking = namedtuple('Booking', ['eventId', 'eventSummary', 'description', 'startTime'])

def make_booking(username, email, avail_times):
    '''
    Updates existing event/slot using eventId and add students as attendee.
    Adds username to summary and changes description.
    '''
    if not avail_times:
        print(colors['RED'],'[>]There are no slots available for booking.')
        return '', '', '', ''
    else:

        time_slot = slot(avail_times)
        if not time_slot:
            return Booking('', '', '', '')

        eventId, startTime = time_slot
        event = service.events().get(calendarId='primary', eventId=eventId).execute()

        event.update({
            'attendees': [{'email': f"{event['summary']}@student.wethinkcode.co.za"}, {'email': email}],
            'summary': f"{event['summary']} & {username}",
            'description': description(),
        })

        sendNotification = True
        sendUpdate = 'all'

        updated_event = service.events().update(
            calendarId='primary', eventId=event['id'], body=event,
            sendNotifications=sendNotification, sendUpdates=sendUpdate
        ).execute()
        print(colors['GREEN'], "[>] You have successfully made your booking.", colors['END'])

        return Booking(
            eventId=updated_event['id'],
            eventSummary=updated_event['summary'],
            description=updated_event['description'],
            startTime=startTime,
        )

