import speech_recognition as sr
from datetime import datetime
import pyttsx3
import json
import re


class FlightBookingAgent:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Mock flight database
        self.flights_db = {
            "flights": [
                {
                    "id": "FL001",
                    "from": "New York",
                    "to": "London",
                    "date": "2025-02-20",
                    "price": 450,
                    "seats_available": 32
                },
                # Add more flights as needed
            ]
        }

        # Conversation state management
        self.booking_state = {
            "origin": None,
            "destination": None,
            "date": None,
            "passengers": None
        }

    def speak(self, text):
        """Convert text to speech"""
        print(f"Agent: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for user input and convert speech to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech recognition service.")
            return None

    def extract_location(self, text):
        """Extract location names from user input"""
        # Add your location extraction logic here
        # This could use NER models or a database of city names
        cities = ["new york", "london", "paris", "tokyo"]  # Example cities
        found_cities = [city for city in cities if city in text.lower()]
        return found_cities[0] if found_cities else None

    def extract_date(self, text):
        """Extract date from user input"""
        # Add date extraction logic
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        match = re.search(date_pattern, text)
        return match.group(0) if match else None

    def extract_passengers(self, text):
        """Extract number of passengers from user input"""
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None

    def search_flights(self):
        """Search for flights based on booking state"""
        available_flights = []
        for flight in self.flights_db["flights"]:
            if (flight["from"].lower() == self.booking_state["origin"] and
                    flight["to"].lower() == self.booking_state["destination"] and
                    flight["date"] == self.booking_state["date"] and
                    flight["seats_available"] >= self.booking_state["passengers"]):
                available_flights.append(flight)
        return available_flights

    def process_booking(self):
        """Main booking flow"""
        self.speak("Welcome to AI Flight Booking Assistant. How can I help you today?")

        # Get origin
        while not self.booking_state["origin"]:
            self.speak("Where would you like to fly from?")
            user_input = self.listen()
            if user_input:
                self.booking_state["origin"] = self.extract_location(user_input)

        # Get destination
        while not self.booking_state["destination"]:
            self.speak("What's your destination?")
            user_input = self.listen()
            if user_input:
                self.booking_state["destination"] = self.extract_location(user_input)

        # Get date
        while not self.booking_state["date"]:
            self.speak("When would you like to travel? Please specify the date in YYYY-MM-DD format.")
            user_input = self.listen()
            if user_input:
                self.booking_state["date"] = self.extract_date(user_input)

        # Get number of passengers
        while not self.booking_state["passengers"]:
            self.speak("How many passengers are traveling?")
            user_input = self.listen()
            if user_input:
                self.booking_state["passengers"] = self.extract_passengers(user_input)

        # Search and present flights
        available_flights = self.search_flights()
        if available_flights:
            self.speak(f"I found {len(available_flights)} flights matching your criteria.")
            for flight in available_flights:
                self.speak(
                    f"Flight {flight['id']} from {flight['from']} to {flight['to']} on {flight['date']} for ${flight['price']} per person.")

            # Handle booking confirmation
            self.speak("Would you like to proceed with booking? Say yes or no.")
            user_input = self.listen()
            if user_input and "yes" in user_input.lower():
                # Add booking confirmation logic here
                self.speak("Great! Your booking is confirmed. You will receive an email with the details shortly.")
            else:
                self.speak("Thank you for using our service. Have a great day!")
        else:
            self.speak("Sorry, no flights found matching your criteria.")


# Example usage
if __name__ == "__main__":
    agent = FlightBookingAgent()
    agent.process_booking()