import os
import random
from functools import lru_cache
import spacy
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

nlp = spacy.load("en_core_web_md")

class Chatbot:
    def __init__(self):
        self.destinations = ["Paris", "Tokyo", "New York", "London", "Berlin"]
        self.activities = ["museums", "parks", "restaurants", "historical sites", "shopping"]

    @lru_cache(maxsize=128)  # Caching for understand function
    def understand(self, message):
        doc = nlp(message)
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        return entities

    def recommend(self, entities):
        response = ""
        if 'GPE' in entities:
            response += f"How about visiting {random.choice(self.destinations)}? "
        else:
            response += f"How about visiting {random.choice(self.destinations)}? "
        
        response += f"I recommend checking out the {random.choice(self.activities)} there."
        return response

    def handle_reservation(self, destination, date):
        # This function might benefit from caching if you implement dynamic inputs and checks
        return f"Reservation for {destination} on {date} confirmed!"

    def reply(self, message):
        entities = self.understand(message)
        
        if "book" in message.lower() or "reserve" in message.lower():
            # For a more advanced scenario, you might want to dynamically parse and use these arguments
            return self.handle_reservation("Paris", "2023-07-20")
        return self.recommend(entities)

if __name__ == "__main__":
    bot = Chatbot()
    user_message = "I want to book a trip to Paris"
    print(bot.reply(user_message))