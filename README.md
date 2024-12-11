# Astro-Bot: Astrological Telegram Bot

## Project Goals
- Create a Telegram bot for personalized astrological forecasts.
- Operate on a monthly subscription basis.
- Interactive, trust-based interaction with the user.

## Architecture and Technologies
- Language: Python 3
- Telegram Bot Framework: `python-telegram-bot`
- API for astrological calculations: initially using OpenAI API for generating text descriptions, with the possibility of connecting specialized astrological APIs later.
- Data Storage: PostgreSQL or SQLite (SQLite can be used for simplicity in early stages).
- Hosting: locally during development, later possibly on Heroku or Render.
- Subscription Payment: Using Telegram Payments or Stripe (to be determined later).
- Gamification: accumulation of bonus points, additional reports, missions.

## Main Functionality:
- User registration with input of name, date, time, and place of birth.
- Generation of a natal chart and its main description.
- Daily sending of personalized forecasts.
- Subscription model: monthly renewal.
- Gamification (missions, bonuses).

## Code Structure (preliminary):
- `bot/` - bot code
  - `main.py` - entry point
  - `handlers/` - command and message handlers
  - `services/` - logic for interacting with APIs and the database
  - `models/` - data models (if using ORM)
- `scripts/` - scheduled scripts (e.g., daily mailing)
- `tests/` - tests

## Database Schema

We use SQLAlchemy with SQLite for development.

**Tables:**
- `users`: Stores user info including birth details.
- `subscriptions`: Tracks user subscription periods and status.
- `user_events`: Logs user-related events (daily predictions sent, missions completed).
- `bonus_points`: Tracks user's bonus point balance.
- `daily_predictions`: Optionally store daily predictions for reference.

See `bot/models/models.py` for detailed schema.

## OpenAI Integration

We use the OpenAI API to generate natal chart descriptions and daily forecasts.

- `bot/services/openai_service.py` contains functions:
  - `generate_natal_chart_description(name, birthdate, birthtime, birthplace)`: returns a textual interpretation of a natal chart.
  - `generate_daily_prediction(name)`: returns a personalized daily forecast.

To test the integration:
```bash
python3 test_openai_service.py
```

#### 5. Commit Your Changes (If Using Git)

```bash
git add .
git commit -m "Add OpenAI integration for natal chart and daily forecasts"
