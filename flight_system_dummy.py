from dummy_data import flights

def search_flights_api(source: str, destination: str, date: str) -> str:

    search_response = ""
    count = 0
    for flight in flights:
      flight_source=flight.get("departure_city");
      flight_destination=flight.get("arrival_city");
      flight_date = flight.get("departure_datetime");   ## logic pending start and end dates

      if flight_source==source and flight_destination==destination:
        count += 1
        search_response += (
            f"Flight: {flight['flight_id']}\n"
            f"Departure: {flight['departure_datetime']}\n"
            f"Arrival: {flight['arrival_datetime']}\n"
            f"Price: {flight['price']}\n"
            f"Seats Available: {flight['available_seats']}\n"
            f"------------------------\n"
        )

    response = f"Found {count} flights from {source} to {destination} on {date}:\n\n" + search_response
    return response
