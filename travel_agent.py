from openai import OpenAI
import json
from datetime import datetime
from typing import Dict, Any
# action , sentiment, source , destination, date
from dummy_data import flights
from flight_system_dummy import search_flights_api;
from datetime import datetime

# Get today's date
current_date = datetime.now().date()
# Format it as a string
current_date_str = str(current_date)

class TravelAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.context = []

    def get_response(self, user_input: str) -> str:
        # Add user input to context
        self.context.append({"role": "user", "content": user_input})

        # Get AI response
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": """You are a travel agent assistant. Extract details in JSON format when available:

                For searching flights:
                {
                    "action": "search_flights",
                    "source": "city",
                    "destination": "city",
                    "date": "YYYY-MM-DD"
                }

                For booking flights:
                {
                    "action": "book_flight",
                    "source": "city",
                    "destination": "city",
                    "flight_date": "YYYY-MM-DD",
                    "flight_time": "HH:MM",
                    "num_passengers": number
                }

                For canceling flights:
                {
                    "action": "cancel_flight",
                    "booking_id": "booking_id"
                }

                Please answer keeping in mind that the current date is {current_date_str}.
                Only extract when all required details are available. Otherwise, ask for missing information.
                For search, ask for source, destination and date if not provided.
                For cancellation, ask for booking ID if not provided."""
            }] + self.context,
            temperature=0.7,
            max_tokens=150
        )

        assistant_response = response.choices[0].message.content

        # Try to parse action details if present
        try:
            action_data = json.loads(assistant_response)

            if action_data.get("action") == "search_flights":
                # Handle flight search
                search_result = self.search_flights(
                    source=action_data["source"],
                    destination=action_data["destination"],
                    date=action_data["date"]
                )
                assistant_response = search_result

            elif action_data.get("action") == "book_flight":
                # Handle flight booking
                booking_result = self.book_flight(
                    source=action_data["source"],
                    destination=action_data["destination"],
                    flight_date=action_data["flight_date"],
                    flight_time=action_data["flight_time"],
                    num_passengers=action_data["num_passengers"]
                )
                assistant_response = booking_result

            elif action_data.get("action") == "cancel_flight":
                # Handle flight cancellation
                cancellation_result = self.cancel_flight(
                    booking_id=action_data["booking_id"]
                )
                assistant_response = cancellation_result

        except json.JSONDecodeError:
            # Not an action, just continue with normal response
            pass

        self.context.append({"role": "assistant", "content": assistant_response})
        return assistant_response

    def search_flights(self, source: str, destination: str, date: str) -> str:
        try:
            # Validate inputs
            if not all([source, destination, date]):
                return "Error: Source, destination and date are required for flight search"

            # Mock flight data - in a real application, this would come from an API or database

            # Format the response
            # response = f"Found {len(flights)} flights from {source} to {destination} on {date}:\n\n"
            #
            # for flight in flights:
            #     response += (
            #         f"Flight: {flight['flight_number']}\n"
            #         f"Departure: {flight['departure_time']}\n"
            #         f"Arrival: {flight['arrival_time']}\n"
            #         f"Price: {flight['price']}\n"
            #         f"Seats Available: {flight['seats_available']}\n"
            #         f"------------------------\n"
            #     )

            response = search_flights_api(source, destination, date)
            response += "\nTo book a flight, please provide the number of passengers and preferred flight time."

            return response

        except Exception as e:
            return f"Error searching flights: {str(e)}"

    def book_flight(self, source: str, destination: str, flight_date: str,
                    flight_time: str, num_passengers: int) -> str:
        try:
            # Validate inputs
            if not all([source, destination, flight_date, flight_time]):
                return "Error: All fields (source, destination, date, time) are required"

            if num_passengers < 1:
                return "Error: Number of passengers must be at least 1"

            # Create booking details dictionary
            booking_details = {
                "source": source.strip(),
                "destination": destination.strip(),
                "flight_date": flight_date,
                "flight_time": flight_time,
                "num_passengers": num_passengers,
                "booking_id": f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "booking_timestamp": datetime.now().isoformat()
            }

            # Here you would typically:
            # 1. Check flight availability
            # 2. Calculate total price
            # 3. Save to database
            # 4. Generate actual booking confirmation

            # For now, return a formatted response
            return (f"Flight booked successfully!\n"
                    f"Booking ID: {booking_details['booking_id']}\n"
                    f"From: {booking_details['source']}\n"
                    f"To: {booking_details['destination']}\n"
                    f"Date: {booking_details['flight_date']}\n"
                    f"Time: {booking_details['flight_time']}\n"
                    f"Passengers: {booking_details['num_passengers']}")

        except Exception as e:
            return f"Error booking flight: {str(e)}"

    def cancel_flight(self, booking_id: str) -> str:
        try:
            # Validate booking ID format
            if not booking_id.startswith("BK"):
                return "Error: Invalid booking ID format. Booking IDs should start with 'BK'"

            # Create cancellation details
            cancellation_details = {
                "booking_id": booking_id,
                "cancellation_timestamp": datetime.now().isoformat(),
                "status": "cancelled"
            }

            # Here you would typically:
            # 1. Verify booking exists
            # 2. Check cancellation policy
            # 3. Process refund if applicable
            # 4. Update booking status in database

            # For now, return a formatted response
            return (f"Flight cancellation successful!\n"
                    f"Booking ID: {cancellation_details['booking_id']}\n"
                    f"Cancellation Time: {cancellation_details['cancellation_timestamp']}\n"
                    f"Status: {cancellation_details['status']}")

        except Exception as e:
            return f"Error cancelling flight: {str(e)}"

    def reschedule_flight(self, booking_id: str, new_date: str) -> str:
        # Implement actual rescheduling logic here
        return f"Flight with booking ID {booking_id} has been rescheduled to {new_date}"

    def get_booking_details(self, booking_id: str) -> str:
        # Implement actual booking retrieval logic here
        return f"Retrieved booking details for ID {booking_id}"