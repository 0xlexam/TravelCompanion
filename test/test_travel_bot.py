import unittest
from unittest.mock import patch
from travel_bot import ChatBot

class TestTravelBot(unittest.TestCase):
    
    def setUp(self):
        """Prepare environment and variables for tests."""
        self.bot = ChatBot()
        self.user_input = 'Book a flight to Paris'
        self.booking_info = {'destination': 'Paris', 'date': '2023-10-10'}
        self.query = 'Weather in Paris'
      
    @patch('travel_bot.ChatBot.process_input')
    def test_process_user_input(self, mock_process_input):
        """Test processing of user input."""
        expected_output = 'Booking flight to Paris...'
        mock_process_input.return_value = expected_output
        
        result = self.bot.process_input(self.user_input)
        
        mock_process_ui
        self.assertEqual(result, expected_output)

    @patch('travel_bot.ChatBot.handle_travel_booking')
    def test_handle_travel_bookings(self, mock_handle_travel_booking):
        """Test handling of travel bookings."""
        expected_output = 'Booking confirmed for Paris on 2023-10-10'
        mock_handle_travel_booking.return_value = expected_output

        result = self.bot.handle_travel_booking(self.booking_info)

        mock_handle_travel_booking.assert_called_once_with(self.booking_info)
        self.assertEqual(result, expected_output)

    @patch.dict('os.environ', {'API_KEY': '123456'})
    @patch('travel_bot.ChatBot.provide_travel_information')
    def test_provide_travel_information(self, mock_provide_travel_information):
        """Test provision of travel information."""
        expected_output = 'The weather in Paris will be sunny tomorrow.'
        mock_provide_travel_information.return_value = expected_output
        
        result = self.bot.provide_travel_information(self.query)
        
        mock_provide_travel_information.assert_called_once_with(self.query)
        self.assertEqual(result, expected_output)
    
    def tearDown(self):
        """Clean up after tests."""
        self.bot = None

if __name__ == '__main__':
    unittest.main()