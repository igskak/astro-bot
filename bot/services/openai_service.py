import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_natal_chart_description(name: str, birthdate: str, birthtime: str, birthplace: str) -> str:
    """
    Uses OpenAI API to generate a natal chart interpretation given user's birth details.
    """
    messages = [
        {"role": "system", "content": "You are a friendly and the smartest astrologer in the world."},
        {
            "role": "user",
            "content": (
                f"A user named {name} was born on {birthdate} at {birthtime} in {birthplace}. "
                "Based on these birth details, provide a concise interpretation of their natal chart. "
                "Include key personality traits and life themes. Keep the tone warm, encouraging, and trustworthy. Respond in the language of user's {name} with maximum of 500 tokens "
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",  # or any other available model
        messages=messages,
        max_tokens=600,
        temperature=0.7
    )

    description = response.choices[0].message.content.strip()
    return description


def generate_daily_prediction(name: str) -> str:
    """
    Uses OpenAI API to generate a daily forecast for the user.
    """
    messages = [
        {"role": "system", "content": "You are a friendly and the smartest astrologer in the world."},
        {
            "role": "user",
            "content": (
                f"The user's name is {name}. Provide a short, personalized daily astrological "
                "forecast. Include a helpful tip or positive affirmation for the day. Use the language of his {name}. Maximum 200 tokens"
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",  # or any other available model
        messages=messages,
        max_tokens=250,
        temperature=0.7
    )

    daily_forecast = response.choices[0].message.content.strip()
    return daily_forecast
