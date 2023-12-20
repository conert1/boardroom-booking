def open_calendar_txt():
    '''
    Opens generated text file containing event info for the calendar.
    Returns list containing the data.
    '''
    file = open('.calendar.txt', 'r')
    calendar_data = file.readlines()

    return calendar_data

def sort_calendar_elements(data):
    '''
    Sorts calendar data into lists of date, time, summary and event description.
    '''
    dates, times, summaries, descriptions = [], [], [], []
    
    for i in data:
        d =  i.strip('\n').split(",")[0]
        s =  i.strip('\n').split(",")[1]
        ed =  i.strip('\n').split(",")[2]

        date = d.split("T")[0]
        time = d.split("T")[1].split('+')[0]
        
        dates.append(date)
        times.append(time)
        summaries.append(s)
        descriptions.append(ed)

    return dates, times, summaries, descriptions

