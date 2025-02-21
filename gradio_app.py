import gradio as gr
from travel_agent_new import TravelAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize travel agent
agent = TravelAgent(api_key)


def respond(message, history):
    """
    Process user message and return agent's response
    """
    # Get response from travel agent
    bot_response = agent.get_response(message)
    return bot_response


def create_demo():
    # Custom CSS for dark theme adjustments
    custom_css = """
    .dark-theme {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    """

    chat_interface = gr.ChatInterface(
        respond,
        chatbot=gr.Chatbot(
            height=600,
            show_copy_button=True,
            bubble_full_width=False,
            container=True,
        ),
        title="✈️ AI Travel Assistant",
        description="""Welcome to the AI Travel Assistant! I can help you with:
        • Searching available flights
        • Booking flights
        • Canceling flights
        • Rescheduling flights
        • Getting booking details

        Just tell me what you need in natural language!""",
        #theme="dark",
        examples=[
            ["Search for flights from New York to London next week"],
            ["I want to book a flight from Paris to Tokyo"],
            ["Cancel my flight with booking ID BK20240315123456"],
            ["Show me my booking details for BK20240315123456"],
        ]
    )

    return chat_interface


if __name__ == "__main__":
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
    else:
        # Create and launch the demo
        demo = create_demo()
        demo.launch(
            share=False,  # Set to True if you want to generate a public link
            server_name="0.0.0.0",
            server_port=7860,
            inbrowser=True
        )