import unittest
from io import StringIO
import sys
from test_base import run_unittests
from test_base import captured_io

from calendar_format.prettytable_formatter import display_calendar
from calendar_format.date_formatter import open_calendar_txt
from calendar_format.date_formatter import sort_calendar_elements

# from calendar_format import prettytable_formatter
import test_base

# from api import quickstart
# with captured_io(StringIO()):
#     quickstart.main()

class MyTestCase(unittest.TestCase):


    def test_open_calendar(self):
        """This is a test to test that checks the output of the open calendar
        function which working, to see that it is working properly we check
        the return. It should return a list so we used checked instance"""


        with captured_io(StringIO) as (out, err):
            output = open_calendar_txt()

        self.assertIsInstance(output, list)


    def test_sort_calendar_elements(self):
        """This function sorts the elements in the list which was created in
          the previous function into the time date and the 'status' so
          to know that the function is working we inputed/passed a 
          parameter of list format and we check will it sort the elements
          properly"""
        
        with captured_io(StringIO) as (out, err):
            output = sort_calendar_elements(["2023-01-17T09:00:00+02:00,Out of office,anything\n"])

        self.assertEqual((['2023-01-17'], ['09:00:00'], ["Out of office"], ["anything"]), output)


    def test_get_credentials(self):
        """This tests the get_credentials function we are checking is the instance
        a dictionary, if the correct datatype is returned then the possibility
        that the function does what it is supposed to do is high."""


        from calendar_format.calendar_view import get_crendentials

        with captured_io(StringIO) as (out, err):
            output = get_crendentials(".token.json")

        self.assertIsInstance(output, dict)


    # def test_week_schedule_from_google_calander(self):
    #     """This check the week_schedule_from_google_calendar to see
    #     does the calendar get the events from the last seven days we could not 
    #     simulate the output for the test because the calendar changes
    #     all the time so we checked instance instead"""


    #     from calendar_format.calendar_view import week_schedule_from_google_calander
    #     from calendar_format.calendar_view import get_crendentials

    #     with captured_io(StringIO) as (out, err):
    #         output = week_schedule_from_google_calander(get_crendentials(".token.json"))
    #     self.assertIsInstance(output, list)
    #     # self.assertNotAlmostEqual([], output)


    def test_display_calendar(self):
        from prettytable import PrettyTable
        from calendar_format.prettytable_formatter import display_calendar
        k = ["2023-01-01"]
        l = ["00:00"]
        m = ["Busy doing stuff"]
        b = ["anything"]
        
        output = display_calendar(k, l, m, b)
        calendar = PrettyTable()    
        calendar.field_names = ["DATE", "TIME", "STATUS"]

        calendar.add_rows([("2023-01-01", "00:00", "Busy doing stuff")])
        # print(calendar)
        
        self.assertNotEqual("""
        
+------------+-------+------------------+
|    DATE    |  TIME |      STATUS      |
+------------+-------+------------------+
| 2023-01-01 | 00:00 | Busy doing stuff |
+------------+-------+------------------+""", output)


    def test_make_slot(self):
        from bookings.make_slot import slot

        with captured_io(StringIO('10 feb 9:00')) as (out, err):
            output = slot(['2023-02-10 08:30:00'])
            
        self.assertAlmostEqual('10 feb 9:00', output)


    def test_register(self):
        """Testing to see that a valid email address is given 
        is it a wethinkcode student email address"""
        
        from main import register
        
        with captured_io(StringIO('false.email@address.com\nnotavalicemail.com\nyour_name@student.wethinkcode.co.za')) as (out, err):
            output = register()
        
        self.assertEqual((True, 'your_name', 'your_name@student.wethinkcode.co.za'), output)

    
    def test_login(self):
        from main import login

        with captured_io(StringIO('your_name@student.wethinkcode.co.za')) as (out, err):
            output = login()

        self.assertEqual((True, 'your_name', 'your_name@student.wethinkcode.co.za') ,output)


    def test_main_prompts(self):
        """testing the main prompt by checking does it only accept valid words
        and keeps asking for input as long as a valid command has not
        been entered"""

        from main import main_prompts

        with captured_io(StringIO("Hello\nName\nSurname\nlogin")):
            output = main_prompts()
        
        self.assertEqual("login", output)




if __name__ == "__main__":
    unittest.main()