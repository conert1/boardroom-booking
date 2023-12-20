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


def create_database():
    '''
    Creates a database which will store all parameters needed to create/update events.
    Columns include: username, email, start_time, eventId, eventSummary and eventDescription.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute('''CREATE TABLE IF NOT EXISTS event_info(
        username text, email text, start_time text, eventId text, 
        eventSummary text, eventDescription text,
        PRIMARY KEY (username, eventId, eventDescription))''')

    con.commit()
    con.close()


def register_user(username, email):
    '''
    Add user to database.
    Updates their username and email.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    exists = cursor_object.execute(f'''SELECT EXISTS(
        SELECT 1 FROM event_info WHERE username = "{username}")''').fetchone()
    if exists == (1,):
        print(colors['GREEN'],'[>] You are already registered and logged in. You may continue.', colors['END'])
    else:
        cursor_object.execute('INSERT INTO event_info(username, email) VALUES(?, ?)', 
            (username, email))
        print(colors['BLUE'], '[>] You have successfully registered on the Code Clinic \
Booking System.', colors['END'])

    con.commit()
    con.close()
    return


def login_user(username):
    '''
    Checks if user is in database and returns true is they are.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    exists = cursor_object.execute(f'''SELECT EXISTS(
        SELECT 1 FROM event_info WHERE username = "{username}")''').fetchone()

    if exists == (1,):
        print(colors['YELLOW'], '[>] You have successfully logged onto the Code Clinic \
Booking System.', colors['END'])
        con.commit()
        con.close()
        return True

    con.commit()
    con.close()


def create_slot_update(username, start_time, eventId):
    '''
    Updates datatable to add start_time, eventId, eventSummary and eventDescription
    using the username as a key.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    """
    sql = f'''INSERT INTO event_info 
                SET start_time = '{start_time}',
                    eventId = '{eventId}',
                    eventSummary = '{eventSummary}'
                WHERE 
                    username = "{username}"'''
    cursor_object.execute(sql)
    """
    cursor_object.execute(f'UPDATE event_info SET start_time = "{start_time}" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventId = "{eventId}" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventSummary = "{username}" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventDescription = "Volunteer available!" \
        WHERE username = "{username}"')

    con.commit()
    con.close()


def book_slot_update(username, start_time, eventId, eventSummary, eventDescription):
    '''
    Updates datatable to add start_time, eventId, eventSummary and eventDescription
    using the username as a key.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'UPDATE event_info SET start_time = "{start_time}" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventId = "{eventId}" \
        WHERE username = "{username}"')

    cursor_object.execute(f'UPDATE event_info SET eventSummary = "{eventSummary}" \
        WHERE eventId = "{eventId}"')
    cursor_object.execute(f'UPDATE event_info SET eventDescription = "{eventDescription}" \
        WHERE eventId = "{eventId}"')
    con.commit()
    con.close()


def cancel_booking_update(username):
    '''
    Updates datatable for students to remove start_time, eventId, 
    eventSummary and eventDescription using the username as a key.
    Also updates eventSummary and eventDescription in volunteer row. 
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'UPDATE event_info SET start_time = ""\
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventId = "" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventSummary = "" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventDescription = "" \
        WHERE username = "{username}"')
    con.commit()
    con.close()


def cancel_booking_update_vol(eventId, eventSummary):
    '''
    Updates datatable for students to remove start_time, eventId, 
    eventSummary and eventDescription using the username as a key.
    Also updates eventSummary and eventDescription in volunteer row. 
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()

    cursor_object.execute(f'UPDATE event_info SET eventSummary = "{eventSummary.split(" &")[0]}" \
        WHERE eventId = "{eventId}"')
    cursor_object.execute(f'UPDATE event_info SET eventDescription = "Volunteer available!" \
        WHERE eventId = "{eventId}"')

    con.commit()
    con.close()


def cancel_slot_update(username):
    '''
    Updates datatable for volunteer to remove start_time, eventId, 
    eventSummary and eventDescription using the username as a key.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'UPDATE event_info SET start_time = ""\
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventId = "" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventSummary = "" \
        WHERE username = "{username}"')
    cursor_object.execute(f'UPDATE event_info SET eventDescription = "" \
        WHERE username = "{username}"')    

    con.commit()
    con.close() 


def remove_user(username):
    '''
    Updates datatable for volunteer to remove start_time, eventId, 
    eventSummary and eventDescription using the username as a key.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'DELETE FROM event_info WHERE username = "{username}"')

    con.commit()
    con.close()      


def check_vol(username):
    '''
    Checks if user has already volunteered for the week.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    exists = cursor_object.execute(f'''SELECT EXISTS(
        SELECT 1 FROM event_info WHERE username = "{username}")''').fetchone()

    if exists == (1,):
        print(colors['RED'], '[>] You have already booked a volunteer slot for the week.', colors['END'])
        con.commit()
        con.close()
        return True

    con.commit()
    con.close()

def get_vol_times():
    '''
    Collects start_times from database to ensure volunteers don't double book a slot.
    '''
    avail_times = []
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute('SELECT start_time FROM event_info')

    times = cursor_object.fetchall()
    for time in times:
        avail_times.append(time[0])

    con.commit()
    con.close()

    return avail_times


def get_avail_times():
    '''
    Collects start_times from database to ensure students don't double book a slot.
    Only collects start_times where & in eventSummary.
    '''
    
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute('''SELECT eventId, start_time FROM event_info WHERE eventDescription = 'Volunteer available!' ''')

    times = cursor_object.fetchall()

    con.commit()
    con.close()

    return times


def cancel_booking_id(username):
    '''
    Gets relevant eventId for username.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'''SELECT eventId, eventSummary FROM event_info WHERE username = '{username}' ''')

    id = cursor_object.fetchone()
    try:
        if username == id[1].split('& ')[1]:
            con.commit()
            con.close()
            return id[0]
    except:
        print(colors['RED'],"[>]You do not have a booking to cancel." ,colors['END'])
        return ''


def cancel_booking_id(username):
    '''
    Gets relevant eventId for username.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'''SELECT eventId, eventSummary FROM event_info WHERE username = '{username}' ''')

    id = cursor_object.fetchone()
    if id != None:
        if username == id[1].split('& ')[1]:
            con.commit()
            con.close()
            return id[0]

    else:
        con.commit()
        con.close()
        print(colors['RED'],"[>]You do not have a booking to cancel." ,colors['END'])
        return ''


def cancel_slot_id(username):
    '''
    Gets relevant eventId for username.
    '''
    con = sqlite3.connect('.ccdatabase.db')
    cursor_object = con.cursor()
    cursor_object.execute(f'''SELECT eventId FROM event_info WHERE username = '{username}' ''')

    id = cursor_object.fetchone()[0]
    if id:
        con.commit()
        con.close()
        return id
    else:
        con.commit()
        con.close()
        return ''


create_database()
