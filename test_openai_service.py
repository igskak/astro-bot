from bot.services.openai_service import generate_natal_chart_description, generate_daily_prediction

def main():
    # Test with mock data for natal chart description
    natal_desc = generate_natal_chart_description(
        name="Alice",
        birthdate="1990-04-15",
        birthtime="14:30",
        birthplace="New York, USA"
    )
    print("Natal Chart Description:\n", natal_desc)

    # Test with mock data for daily forecast
    daily_forecast = generate_daily_prediction(name="Alice")
    print("\nDaily Forecast:\n", daily_forecast)

if __name__ == "__main__":
    main()