import unittest
from unittest.mock import patch
from travel_bot import ChatBot

class TestTravelBot(unittest.TestCase):
    
    def setUp(self):
        self.chat_bot = ChatBot()
        self.user_flight_booking_request = 'Book a flight to Paris'
        self.flight_booking_details = {'destination': 'Paris', 'date': '2023-10-10'}
        self.weather_query_request = 'Weather in Paris'
      
    @patch('travel_bot.ChatBot.process_user_message')
    def test_process_user_message(self, mock_process_user_message):
        expected_response = 'Booking flight to Paris...'
        mock_process_user_message.return_value = expected_response
        
        process_result = self.chat_bot.process_user_message(self.user_flight_booking_request)
        
        self.assertEqual(process_result, expected_response)

    @patch('travel_bot.ChatBot.execute_flight_booking')
    def test_execute_flight_booking(self, mock_execute_flight_booking):
        expected_booking_confirmation = 'Booking confirmed for Paris on 2023-10-10'
        mock_execute_flight_booking.return_value = expected_booking_confirmation

        booking_result = self.chat_bot.execute_flight_booking(self.flight_booking_details)

        mock_execute_flight_booking.assert_called_once_with(self.flight_booking_details)
        self.assertEqual(booking_result, expected_booking_confirmation)

    @patch.dict('os.environ', {'API_KEY': '123456'})
    @patch('travel_bot.ChatBot.fetch_travel_info')
    def test_fetch_travel_path_info(self, mock_fetch_travel_info):
        expected_weather_info = 'The weather in Paris will be sunny tomorrow.'
        mock_fetch_travel_info.return_value = expected_weather_info
        
        info_result = self.chat_bot.fetch_travel_info(self.weather_query_request)
        
        mock_fetch_travel_info.assert_called_once_with(self.weather_query_request)
        self.assertEqual(info_result, expected_weather_info)
    
    def tearDown(self):
        self.chat_bot = None

if __name__ == '__main__':
    unittest.main()