import unittest
from unittest.mock import patch
from travel_bot import ChatBot

class TestTravelBot(unittest.TestCase):
    def setUp(self):
        self.bot = ChatBot()

    @patch('travel_bot.ChatBot.process_input')
    def test_process_user_input(self, mock_process_input):
        user_input = 'Book a flight to Paris'
        expected_output = 'Booking flight to Paris...'
        mock_process_input.return_value = expected_output
        self.assertEqual(self.bot.process_input(user_input), expected_output)

    @patch('travel_bot.ChatBot.handle_travel_booking')
    def test_handle_travel_bookings(self, mock_handle_travel_booking):
        booking_info = {'destination': 'Paris', 'date': '2023-10-10'}
        expected_output = 'Booking confirmed for Paris on 2023-10-10'
        mock_handle_travel_booking.return_value = expected_output
        self.assertEqual(self.bot.handle_travel_booking(booking_info), expected_output)
    
    @patch.dict('os.environ', {'API_KEY': '123456'})
    @patch('travel_bot.ChatBot.provide_travel_information')
    def test_provide_travel_information(self, mock_provide_travel_information):
        query = 'Weather in Paris'
        expected_output = 'The weather in Paris will be sunny tomorrow.'
        mock_provide_travel_information.return_value = expected_output
        self.assertEqual(self.bot.provide_travel_information(query), expected_output)

    def tearDown(self):
        self.bot = None

if __name__ == '__main__':
    unittest.main()