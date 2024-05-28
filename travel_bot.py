import os
import random
from functools import lru_cache
import spacy
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")  # Assuming usage in future development
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if WEATHER_API_KEY is None:
    raise ValueError("WEATHER_API_KEY is not set in the environment variables.")

try:
    nlp = spacy.load("en_core_web_md")
except Exception as e:
    raise ImportError(f"Failed to load SpaCy model: {str(e)}")

class Chatbot:
    def __init__(self):
        self.destinations = ["Paris", "Tokyo", "New York", "London", "Berlin"]
        self.activities = ["museums", "parks", "restaurants", "historical sites", "shopping"]

    @lru_cache(maxsize=128)
    def understand(self, message):
        try:
            doc = nlp(message)
            entities = {}
            for ent in doc.ents:
                entities[ent.label_] = ent.text
            return entities
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return {}

    def get_weather_forecast(self, location):
        forecast = "sunny"  # Placeholder forecast
        try:
            # Placeholder for actual weather forecast retrieval logic
            # response = requests.get(f"https://api.example.com/weather?apikey={WEATHER_API_KEY}&location={location}")
            # forecast_data = response.json()
            # forecast = forecast_data.get('forecast', 'sunny')  # Fallback to 'sunny'
            return f"The weather in {location} is expected to be {forecast}."
        except Exception as e:  # Generic exception handling for broad coverage, replace Exception with specific ones as needed.
            print(f"Failed to fetch weather forecast: {str(e)}")
            return "Couldn't fetch the weather forecast, but I'm sure it's nice!"

    def recommend(self, entities):
        response = ""
        location = None
        if 'GPE' in entities:
            location = entities['GPE']
            response += f"How about visiting {location}? "
        else:
            location = random.choice(self.destinations)
            response += f"How about visiting {location}? "
        
        response += f"I recommend checking out the {random.choice(self.activities)} there. "
        
        if location:
            response += self.get_weather_forecast(location)
        return response

    def handle_reservation(self, destination, date):
        # Implement additional error handling here if interacting with APIs or external services.
        return f"Reservation for {destination} on {date} confirmed!"

    def reply(self, message):
        entities = {}
        try:
            entities = self.understand(message)
        except Exception as e:
            return f"Sorry, I couldn't fully understand that. Could you try rephrasing? Error: {str(e)}"
        
        if "book" in message.lower() or "reserve" in message.lower():
            # Implement additional validation or error handling for dates/destinations if needed
            return self.handle_reservation("Paris", "2023-07-20")
        return self.recommend(entities)

if __name__ == "__main__":
    bot = Chatbot()
    user_message = "Tell me about Paris"
    print(bot.reply(user_message))