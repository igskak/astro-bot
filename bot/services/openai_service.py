"""
OpenAI Service Module
This module provides integration with OpenAI's GPT models for generating
astrological predictions and natal chart interpretations.

The service uses GPT-4 to generate human-like, contextually appropriate
astrological content while maintaining a warm and professional tone.

Features:
- Natal chart interpretation generation
- Daily astrological predictions
- Multilingual support (based on user's name context)
- Message translation
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def translate_message(text: str, target_language: str) -> str:
    """
    Translate a message to the target language using OpenAI's GPT-4.

    Args:
        text (str): Text to translate
        target_language (str): Target language code (e.g., 'en', 'es', 'fr')

    Returns:
        str: Translated text
    """
    messages = [
        {"role": "system", "content": "You are a professional translator."},
        {
            "role": "user",
            "content": f"Translate the following text to {target_language}. Keep the same formatting and tone: {text}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500,
        temperature=0.3  # Lower temperature for more accurate translations
    )

    return response.choices[0].message.content.strip()

async def generate_natal_chart_description(name: str, birthdate: str, birthtime: str, birthplace: str, language: str) -> str:
    """
    Generate a personalized natal chart interpretation using OpenAI's GPT-4.

    Args:
        name (str): User's full name
        birthdate (str): Date of birth in ISO format (YYYY-MM-DD)
        birthtime (str): Time of birth in 24-hour format (HH:MM)
        birthplace (str): Place of birth (city, country)
        language (str): Target language code

    Returns:
        str: A detailed interpretation of the user's natal chart
    """
    messages = [
        {
            "role": "system", 
            "content": f"You are a professional astrologer providing natal chart interpretations. Respond in {language}."
        },
        {
            "role": "user",
            "content": (
                f"Generate a natal chart interpretation for {name}, born on {birthdate} at {birthtime} in {birthplace}. "
                "Include personality traits, life themes, and potential opportunities. "
                "Keep the tone warm and encouraging. Maximum 500 words."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=600,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

async def generate_daily_prediction(name: str, language: str) -> str:
    """
    Generate a personalized daily astrological forecast using OpenAI's GPT-4.

    Args:
        name (str): User's full name
        language (str): Target language code

    Returns:
        str: A personalized daily astrological forecast
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a professional astrologer providing daily horoscope readings in {language}. "
                "Format your response exactly like this example:\n\n"
                "🌟 Загальний огляд\n[prediction text]\n\n"
                "❤️ Кохання та стосунки\n[prediction text]\n\n"
                "💼 Кар'єра та цілі\n[prediction text]\n\n"
                "🌿 Здоров'я та самопочуття\n[prediction text]\n\n"
                "✨ Афірмація дня\n[affirmation text]\n\n"
                "Important: Never use ### or other markdown. Use exactly one space between emoji and *text*."
            )
        },
        {
            "role": "user",
            "content": (
                f"Generate a daily astrological forecast for {name}. Make it personal and encouraging."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
