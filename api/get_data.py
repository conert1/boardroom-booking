import requests, json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}

def get_code_clinic_data(calendar_id):
    '''
    Connects to the code clinic given the calendar id.
    Downloads the data and writes it to a json file.
    '''

    api_response = requests.get(f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?key=AIzaSyAfqwO-dl91GO5G1U7kpVlrhv0fAf1Omhw')
    if api_response.status_code == 200:
        print(colors['MAGENTA'],"[>] Successfully connected to the google calendar.", colors['END'])
    else:
        print(f"{api_response.status_code} : Error.")

    # Gets data from API in a dict
    data = api_response.json()
    convert_to_json = json.dumps(data, sort_keys=True, indent=4)

    #creating json file with calendar data?
    with open('calendar_data.json', 'w') as datafile:
        datafile.write(convert_to_json)

def get_student_cal_data(calendar_id):
    '''
    Connects to the student calendar given the calendar id.
    Downloads the data and writes it to a json file.
    '''
    pass

if __name__ == "__main__":
    get_code_clinic_data('jhb3cc@gmail.com')
    # get_student_cal_data('bumokat022@student.wethinkcode.co.za')

