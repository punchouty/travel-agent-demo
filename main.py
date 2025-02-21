from travel_agent import TravelAgent
import os
from dotenv import load_dotenv


def main():
    # Load OpenAI API key from environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        return

    # Initialize the travel agent
    agent = TravelAgent(api_key)

    print("Welcome to AI Travel Assistant!")
    print("How can I help you today?")
    print("(Type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            print("Thank you for using AI Travel Assistant. Goodbye!")
            break

        response = agent.get_response(user_input)
        print(f"\nAssistant: {response}")


if __name__ == "__main__":
    main()