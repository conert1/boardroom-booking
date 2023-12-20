from prettytable import PrettyTable

colors = {
    'BLUE': '\33[1;94m',
    'RED': '\033[1;91m',
    'WHITE': '\33[1;97m',
    'YELLOW': '\33[1;93m',
    'MAGENTA': '\033[1;35m',
    'GREEN': '\033[1;32m',
    'END': '\033[0m',
}

def display_calendar(dates, times, summaries, descriptions):
    '''
    Formats a calendar using prettytable.
    Date, time and Status from date formatter module.
    '''
    calendar = PrettyTable()    
    calendar.field_names = [f"{colors['BLUE']}DATE{colors['END']}", f"{colors['BLUE']}TIME{colors['END']}", f"{colors['BLUE']}SUMMARY{colors['END']}", f"{colors['BLUE']}DESCRIPTION{colors['END']}"]
    for i in range(len(times)):
        calendar.add_row([dates[i], times[i], summaries[i], descriptions[i]])
    return calendar

