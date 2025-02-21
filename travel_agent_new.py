from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from langchain.memory import ConversationBufferMemory
from datetime import datetime
from typing import Optional
import json
from flight_system_dummy import search_flights_api

class TravelAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            temperature=0.7,
            model="gpt-4o-mini"
        )

        # Define tools
        self.tools = [
            StructuredTool.from_function(
                func=self.search_flights,
                name="search_flights",
                description="Search for available flights between cities on a specific date"
            ),
            StructuredTool.from_function(
                func=self.book_flight,
                name="book_flight",
                description="Book a flight with specific details"
            ),
            StructuredTool.from_function(
                func=self.cancel_flight,
                name="cancel_flight",
                description="Cancel a flight booking using booking ID"
            ),
            StructuredTool.from_function(
                func=self.get_booking_details,
                name="get_booking_details",
                description="Get details of a booking using booking ID"
            )
        ]

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful travel assistant that can help with flight bookings, 
             cancellations, and searches. Use the available tools to help users with their requests.
             Always ask for missing information before using tools."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Set up memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Create agent
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)

        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )


    def search_flights(self, source: str, destination: str, date: str) -> str:
        try:
            # Validate inputs
            if not all([source, destination, date]):
                return "Error: Source, destination and date are required for flight search"

            print("****** In Search flight method *******")
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


    # def search_flights_2(
    #         self,
    #         source: str,
    #         destination: str,
    #         date: str
    # ) -> str:
    #     """Search for available flights between cities"""
    #     try:
    #         # Mock flight data
    #         mock_flights = [
    #             {
    #                 "flight_number": "FL001",
    #                 "source": source,
    #                 "destination": destination,
    #                 "date": date,
    #                 "departure_time": "09:00",
    #                 "arrival_time": "11:00",
    #                 "price": "USD 300",
    #                 "seats_available": 45
    #             },
    #             {
    #                 "flight_number": "FL002",
    #                 "source": source,
    #                 "destination": destination,
    #                 "date": date,
    #                 "departure_time": "13:00",
    #                 "arrival_time": "15:00",
    #                 "price": "USD 350",
    #                 "seats_available": 30
    #             }
    #         ]
    #
    #         response = f"Found {len(mock_flights)} flights from {source} to {destination} on {date}:\n\n"
    #         for flight in mock_flights:
    #             response += (
    #                 f"Flight: {flight['flight_number']}\n"
    #                 f"Departure: {flight['departure_time']}\n"
    #                 f"Arrival: {flight['arrival_time']}\n"
    #                 f"Price: {flight['price']}\n"
    #                 f"Seats Available: {flight['seats_available']}\n"
    #                 f"------------------------\n"
    #             )
    #         return response
    #     except Exception as e:
    #         return f"Error searching flights: {str(e)}"

    def book_flight(
            self,
            source: str,
            destination: str,
            flight_date: str,
            flight_time: str,
            num_passengers: int
    ) -> str:
        """Book a flight with the given details"""
        print("********  In booking flight method *********")
        try:
            booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return (
                f"Flight booked successfully!\n"
                f"Booking ID: {booking_id}\n"
                f"From: {source}\n"
                f"To: {destination}\n"
                f"Date: {flight_date}\n"
                f"Time: {flight_time}\n"
                f"Passengers: {num_passengers}"
            )
        except Exception as e:
            return f"Error booking flight: {str(e)}"

    def cancel_flight(
            self,
            booking_id: str
    ) -> str:
        """Cancel a flight booking"""
        try:
            if not booking_id.startswith("BK"):
                return "Error: Invalid booking ID format. Booking IDs should start with 'BK'"

            return (
                f"Flight cancellation successful!\n"
                f"Booking ID: {booking_id}\n"
                f"Cancellation Time: {datetime.now().isoformat()}\n"
                f"Status: cancelled"
            )
        except Exception as e:
            return f"Error cancelling flight: {str(e)}"

    def get_booking_details(
            self,
            booking_id: str
    ) -> str:
        """Get details of a booking"""
        try:
            if not booking_id.startswith("BK"):
                return "Error: Invalid booking ID format"

            # Mock booking details
            return (
                f"Booking Details for {booking_id}:\n"
                f"Status: Confirmed\n"
                f"Passenger Count: 2\n"
                f"Flight: FL001\n"
                f"Date: 2024-03-20"
            )
        except Exception as e:
            return f"Error retrieving booking details: {str(e)}"

    def get_response(self, user_input: str) -> str:
        """Process user input and return response"""
        try:
            response = self.agent_executor.invoke(
                {"input": user_input}
            )
            return response["output"]
        except Exception as e:
            return f"Error processing request: {str(e)}"