import datetime, json, os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import sqlite3


colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}


def header(function):
    """Decorator function to add a heading to the code"""
    def wrapper(*args, **kwargs):
        print(" ------------ Calendar Events of the Last 7 Days ------------ ")
        return function(*args, **kwargs)
    return wrapper


# def save_file(file_path):
#     """
#     Decorator function that saves the return of the calendar function to a file
#     Checks if it exists or not and makes sure not to add duplicate information
#     The wrapper function does all the i/o work.
#     """
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             data = function(*args, **kwargs)
#             if not os.path.isfile(file_path):
#                 with open(file_path, 'w') as f:
#                     f.write(str(data))
#             else:
#                 os.remove(file_path)
#                 with open(file_path, 'w') as f:
#                     f.write(str(data))
#             return data
#         return wrapper
#     return decorator


def get_crendentials(fn):
    """
    Get the crendentials needed to access calendar
    Indentifiers of the things we need from the token.json file
    For-loop to get only those kwarg assigned to args inside the info dict
    """
    with open(fn, 'r') as file:
        data = json.load(file)

    info, identifiers = dict(), ['token', 'refresh_token', 'client_id', 'client_secret', 'token_uri', 'scopes']
    for identifier in identifiers:
        info[identifier] = data[identifier]
    return info


# @save_file(".calendar.txt")

def week_schedule_from_google_calander(credentials):
    """
    Get the build of the calendar service from Google
    Use the kwarg(crendentials) to access the calender
    Get the time in UTC format using Z
    Get the events from the last 7 days
    """

    credential = Credentials.from_authorized_user_info(info=credentials)
    service = build('calendar', 'v3', credentials=credential)

    current_time = datetime.datetime.utcnow().isoformat() + 'Z'

    events_data = service.events().list(calendarId='primary', timeMin=current_time,
                                        timeMax=(datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()+ 'Z', singleEvents=True,
                                        orderBy='startTime').execute()
    weeks_events = events_data.get('items', [])

    # data = []
    file = open('.calendar.txt', 'w')

    for event in weeks_events:
        data = []
        start = event['start'].get('dateTime', event['start'].get('date'))
        try:
            event_des = event['description']
            data.append((start, event["summary"], event_des))
        except (KeyError, ValueError, Exception):
            pass           
            
        for text in data:
            file.write(f"{text[0]},{text[1]},{text[-1]}\n") 

    file.close()
    


def get_cal_data(credentials):
    """
    Get the build of the calendar service from Google
    Use the kwarg(crendentials) to access the calendar
    Get the time in UTC format using Z
    Get the events from the next 7 days
    Store the username, email, eventId, start time, event summary and event description in a SQLite database
    """
    # Set up connection to SQLite database
    conn = sqlite3.connect('.ccdatabase.db')
    c = conn.cursor()

    # Create events table if it doesn't exist

    c.execute('''CREATE TABLE IF NOT EXISTS event_info(
        username text, email text, start_time text, eventId text, 
        eventSummary text, eventDescription text,
        PRIMARY KEY (username, eventId, eventDescription))''')

    # Get credentials and set up Google Calendar service
    credential = Credentials.from_authorized_user_info(info=credentials)
    service = build('calendar', 'v3', credentials=credential)

    current_time = datetime.datetime.utcnow().isoformat() + 'Z'

    # Get events from the last 7 days
    events_data = service.events().list(calendarId='primary', timeMin=current_time,
                                        timeMax=(datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z',
                                        singleEvents=True, orderBy='startTime').execute()
    weeks_events = events_data.get('items', [])


    # Store event data in database
    for event in weeks_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event['summary']
        description = event.get('description', '')

        # Insert event data into events table
        try:
            if '&' not in summary:        
                c.execute("INSERT INTO event_info VALUES (?, ?, ?, ?, ?, ?)", (summary, f'{summary}@student.wethinkcode.co.za', start, event['id'], summary, description))
            elif '&' in summary:
                user1 = summary.split(' & ')[0]
                c.execute("INSERT INTO event_info VALUES (?, ?, ?, ?, ?, ?)", (user1, f'{user1}@student.wethinkcode.co.za',  start, event['id'], summary, description))
                user2 = summary.split(' & ')[1]
                c.execute("INSERT INTO event_info VALUES (?, ?, ?, ?, ?, ?)", (user2, f'{user2}@student.wethinkcode.co.za', start, event['id'], summary, description))
        except:
            pass

    # Commit changes and close database connection
    conn.commit()
    conn.close()

    # print(colors["GREEN"], f"[>] Event data for {len(weeks_events)} events has been stored in the database.", colors['END'])



