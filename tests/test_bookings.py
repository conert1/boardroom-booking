import unittest
from io import StringIO
import sys
from test_base import run_unittests
from test_base import captured_io

from bookings.book_slot import slot
from bookings.book_slot import description

from bookings.book_slot import make_booking

from bookings.cancel_booking import cancel_booking

from bookings.cancel_slot import check_slot
from bookings.cancel_slot import cancel_slot
import test_base
from unittest.mock import patch


avail_times = ['2023-02-10 08:30:00']

class BookingsTestCase(unittest.TestCase):
    

#passing 
    def test_book_slot_1(self):
        '''
        checks if program asks volunteer what time they would like to make a slot.
        '''
        avail_times = ['2023-02-10 08:30:00']
        with captured_io(StringIO('10 feb 2023 9:00')) as (out, err):
            slot(avail_times)
        output = out.getvalue().strip()

        self.assertEqual("""What date and time would you like to book? i.e. 10 feb 2023 8:00:""", output)


# passing 
    def test_book_slot_2(self):
        '''
        checks if program asks volunteer what time they would like to make a slot
        and the volunteer cancels.
        '''

        avail_times = ['2023-02-10 08:30:00']
        with patch('sys.stdin', StringIO("cancel\n")):
            result = slot(avail_times)
       
        self.assertEqual('', result)


#passing 
    def test_book_slot_3(self):
        '''
        checks if program asks volunteer what time they would like to make a slot
        and the selected time is not valid
        '''
        avail_times = ['2023-02-10 08:30:00']
        with captured_io(StringIO('10 feb 2023 19:00')) as (out, err):
            slot(avail_times)
        output = out.getvalue().strip()

        self.assertEqual("""What date and time would you like to book? i.e. 10 feb 2023 8:00:""", output)


# passing 
    def test_description_1(self):
        '''
        Checks if program asks for description.
        '''
        with captured_io(StringIO('while loops')) as (out, err):
            description()
        output = out.getvalue().strip()

        self.assertEqual("""What would you like help with?""", output)

# passing 
    def test_description_2(self):
        '''
        Checks if program asks for description.
        '''
        with captured_io(StringIO('conditionals')) as (out, err):
            description()
        output = out.getvalue().strip()

        self.assertEqual("""What would you like help with?""", output)
        

class CancelSlotTests(unittest.TestCase):

    def test_cancel_slot_1(self):
        '''
        Checks if volunteer can successfully cancel a slot.
        Checks if & is in eventSummary.
        '''
        pass
        # username = 'tamakun022'
        # eventId = "event"
        

        # output = cancel_slot(username, eventId)
        
        # with captured_output() as (out, err):
        #     check_slot(username, eventId)
        

        # output = out.getvalue().strip()
        # expectedOutput = file.read()
        # sendNotification = True
        # sendUpdate = 'all'

        # self.assertTrue(output)

def test_cancel_slot_1(self):
    '''
    Checks output when volunteer fails to cancel a slot.
    Checks if & is in eventSummary.
    '''

        # with captured_output() as (out, err):
        #     check_slot(username, eventId)
        

        # output = out.getvalue().strip()
        # expectedOutput = file.read()
        # sendNotification = True
        # sendUpdate = 'all'

    # self.assertEqual("""You can not cancel your slot because a student has already booked it,
    #     or the slot belongs to another volunteer.""", output)
    pass


if __name__=='__main__':
    unittest.main()
