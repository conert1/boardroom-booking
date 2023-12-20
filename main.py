from api.get_data import *
from api import quickstart 
from calendar_format.calendar_view import *
from calendar_format.date_formatter import *
from calendar_format.prettytable_formatter import *
from database.user_database import *
from prettytable import PrettyTable
import bookings as book
import os

colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}

    
def display_prompts():
    '''
    Tells user available actions.
    '''
    print(f"{colors['GREEN']}You can perform the following actions:{colors['END']}")
    functions = {
        "REGISTER": "register as a first time user.",
        'LOGIN': "access calendars and make/update bookings.",
        'HELP': "display prompts.",
        "VIEW MY CALENDAR": "view your own calendar",
        "VIEW CC CALENDAR": "view code clinic calendar.",
        "VOLUNTEER": "create a slot as a volunteer.",
        "BOOK": "make a booking with a volunteer.",
        "CANCEL SLOT": "cancel a slot as a volunteer.",
        "CANCEL BOOKING": "cancel a booking.",
        "LOGOUT": "logs you out of Code Clinic.",
    }
    helper = PrettyTable()
    helper.field_names = [f"{colors['RED']}Command{colors['END']}", f"{colors['BLUE']}Description{colors['END']}"]
    for key, value in functions.items():
        helper.add_row([f"{colors['RED']}{key}{colors['END']}", f"{colors['BLUE']}{value}{colors['END']}"])
    print(helper)


def register():
    '''
    Returns email address as well as username from user.
    '''
    while True:
        email = input('[>] Please enter your email address to register: \n[>] ').lower()
        if email == 'cancel':
            return False, '', ''

        elif not email or '@student.wethinkcode.co.za' not in email:
            print('''You have entered an invalid email address. 
Use your WeThinkCode_ email or enter cancel to exit registration.''')
            continue

        else:
            if not os.path.isfile('.token.json'):
                quickstart.main()

            register_user(email.split('@')[0], email)
            return True, email.split('@')[0], email


def login():
    '''
    Checks if user is in database.
    If not asks user to register.
    '''
    while True:
        email = input('[>] Please enter your email address to login: \n[>] ').lower()
        logged = login_user(email.split('@')[0])
        
        if not logged:
            print(colors['RED'], '[>] You are not registed.', colors['END'])
            logged, email.split('@')[0], email = register()
            
            return logged, email.split('@')[0], email

        else:
            if not os.path.isfile('.token.json'):
                quickstart.main()
            
            return True, email.split('@')[0], email


def main_prompts():
    '''
    Gets a valid prompt from the user.
    '''
    valid_prompts = ['login', 'register', 'help', 'view my calendar', 
    'view cc calendar', 'volunteer', 'book', 'cancel slot', 
    'cancel booking', 'logout']

    while True:
        prompt = input('[>] What would you like to do? \n[>] ')
        if not prompt or prompt.lower() not in valid_prompts:
            print(colors['YELLOW'], 'You have entered an invalid prompt. You may enter help to see valid prompts.', colors['END'])
            continue
        else:
            return prompt.lower()


def view_my_calendar():
    '''
    Displays student calendar on terminal.
    '''
    credentials = get_crendentials('.token.json')
    week_schedule_from_google_calander(credentials)
    data = open_calendar_txt()
    try:
        dates, times, summaries, descriptions = sort_calendar_elements(data)
        print(display_calendar(dates, times, summaries, descriptions))
    except TypeError:
        print(colors['YELLOW'], 'There are no events to display for the next 7 days.', colors['END'])    


def view_cc_calendar():
    '''
    Displays code clinic calendar on terminal.
    '''
    credentials = get_crendentials(".cctoken.json")
    week_schedule_from_google_calander(credentials)
    data = open_calendar_txt()
    try:
        dates, times, summaries, descriptions = sort_calendar_elements(data)
        print(display_calendar(dates, times, summaries, descriptions))
    except TypeError:
        print(colors['YELLOW'], 'There are no events to display for the next 7 days.', colors['END'])    


def handle_prompt(prompt, logged, username, email, eventId, eventSummary, start_time):
    '''
    Calls different functions for each prompt.
    '''
    def logged_in(username, email, eventId, eventSummary, start_time):
        '''
        Funtion that will allow the user access to the booking system
        only if they are logged in.
        '''

        if prompt == 'help':
            display_prompts()

        elif prompt == 'view my calendar':
            view_my_calendar()

        elif prompt == 'view cc calendar':
            view_cc_calendar()

        elif prompt == 'volunteer':
            avail_times = get_vol_times()
            eventId, eventSummary, start_time = book.create_slot(
                username, email, avail_times)
            if start_time:    
                create_slot_update(username, start_time, eventId)

        elif prompt == 'book':
            avail_times = get_avail_times()
            eventId, eventSummary, eventDescription, start_time = book.make_booking(
                username, email, avail_times)
            if start_time:
                book_slot_update(username, start_time, eventId, eventSummary, eventDescription)
        
        elif prompt == 'cancel booking':
            eventId = cancel_booking_id(username)
            if eventId:
                eventId, eventSummary = book.cancel_booking(username, eventId)
                if eventSummary:
                    cancel_booking_update(username)
                    cancel_booking_update_vol(eventId, eventSummary)
            
        elif prompt == 'cancel slot':
            eventId = cancel_slot_id(username)
            if book.cancel_slot(username, eventId):
                cancel_slot_update(username)

        return eventId, eventSummary, start_time

    if prompt == 'register':
        logged, username, email = register()        

    elif prompt == 'login':
        logged, username, email = login()

    elif prompt == 'logout':
        try:
            os.remove('.token.json')
            os.remove('.ccdatabase.db')
        except:
            pass
        
        logged = False
        return logged, username, email, eventId, eventSummary, start_time

    if logged:
        eventId, eventSummary, start_time = logged_in(username, email, eventId,
        eventSummary, start_time)

    else:
        print(colors['BLUE'], '[>] You are not logged into the Code Clinic Booking System. \
Please enter login or register to continue.', colors['END'])

    return logged, username, email, eventId, eventSummary, start_time


def main():
    '''
    Runs Code Clinic beginning with registration or login.
    '''
    credentials = get_crendentials('.cctoken.json')
    get_cal_data(credentials)

    print(colors['RED'], """
   _   _   _   _     _   _   _   _   _   _   _  
  / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ 
 ( C ( o ( d ( e ) ( C ( l ( i ( n ( i ( c ( s )
  \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/   v1.0.1
    """, colors['END'])
    print(colors['BLUE'],'\nWelcome to the Code Clinic Booking System.\n', colors['END'])

    display_prompts()

    logged = False
    username, email, eventId, eventSummary, start_time = '', '', '', '', ''

    while True:

        prompt = main_prompts()
        if prompt == 'help':
            display_prompts()

        else:
            logged, username, email, eventId, eventSummary, start_time = handle_prompt(
                prompt, logged, username, email, eventId, eventSummary, start_time)
        
            if logged == False:
                print(colors['YELLOW'], '[>] Thank you for using the Code Clinic Booking System!', colors['END'])
                break


if __name__ == "__main__":
    main()
