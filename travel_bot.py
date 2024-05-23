import os
import random
from functools import lru_cache
import spacy
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

nlp = spacy.load("en_core_web_md")

class Chatbot:
    def __init__(self):
        self.destinations = ["Paris", "Tokyo", "New York", "London", "Berlin"]
        self.activities = ["museums", "parks", "restaurants", "historical sites", "shopping"]

    @lru_cache(maxsize=128)
    def understand(self, message):
        doc = nlp(message)
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        return entities
    
    def get_weather_forecast(self, location):
        forecast = "sunny"
        return f"The weather in {location} is expected to be {forecast}. "

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
        return f"Reservation for {destination} on {date} confirmed!"

    def reply(self, message):
        entities = self.understand(message)
        
        if "book" in message.lower() or "reserve" in message.lower():
            return self.handle_reservation("Paris", "2023-07-20")
        return self.recommend(entities)

if __name__ == "__main__":
    bot = Chatbot()
    user_message = "Tell me about Paris"
    print(bot.reply(user_message))