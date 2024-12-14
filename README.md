# Astro-Bot: Astrological Telegram Bot

Version: 1.0.0

## Project Goals
- Create a Telegram bot for personalized astrological forecasts.
- Operate on a monthly subscription basis.
- Interactive, trust-based interaction with the user.

## Features
- ✅ User registration and profile management
- ✅ Birth chart generation and interpretation
- ✅ Daily personalized forecasts
- ✅ Subscription management
- ✅ Automated scheduling system
- ✅ Database integration
- ✅ OpenAI integration for astrological interpretations

## User Flow

### Registration Process
1. Start the bot by sending `/start`
   - If user is new: Begins registration process
   - If user exists: Shows welcome back message with daily forecast option

2. New User Registration Steps:
   - Name input: User provides their name
   - Birth date: User enters birth date in YYYY-MM-DD format (e.g., 1990-04-15)
   - Birth time: User provides birth time in HH:MM format (e.g., 14:30)
   - Birth place: User enters their birth place (e.g., New York, USA)
   - After registration: User receives their natal chart interpretation

### Daily Usage
1. Get Daily Forecast
   - Send `/daily` command
   - Bot checks user registration status
   - If registered: Provides personalized daily forecast
   - If not registered: Prompts to start registration

### Commands
- `/start` - Begin registration or show welcome message
- `/daily` - Get your daily astrological forecast
- `/cancel` - Cancel the current operation (during registration)

## Subscription and Payment

- `/subscribe`: Sends an invoice for a monthly subscription.
- After successful payment:
  - The user's subscription is recorded in the database.
  - `/daily` forecasts become available only if the user has an active subscription.

### Payment Flow
1. User sends `/subscribe`.
2. Bot sends an invoice via Telegram Payments.
3. User pays the invoice.
4. Bot receives a `SUCCESSFUL_PAYMENT` update and activates the subscription for 30 days.
5. The user can now use `/daily` to get daily forecasts.

### Environment Variables
Required variables in `.env`:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `OPENAI_API_KEY`: Your OpenAI API key
- `PAYMENT_PROVIDER_TOKEN`: Payment provider token for subscriptions

## Architecture and Technologies
- Language: Python 3
- Telegram Bot Framework: `python-telegram-bot`
- OpenAI API: For generating astrological interpretations
- Database: SQLite with SQLAlchemy ORM
- Scheduler: Custom scheduling service for automated tasks
- Payment Processing: Telegram Payments integration

## Code Structure
- `bot/` - Main bot code
  - `main.py` - Entry point and bot initialization
  - `handlers/` - Command and message handlers
  - `services/` - Core services:
    - `database.py` - Database operations
    - `openai_service.py` - OpenAI API integration
    - `scheduler_service.py` - Task scheduling
    - `subscription_service.py` - Subscription management
  - `models/` - SQLAlchemy models
- `scripts/` - Utility scripts
- `tests/` - Test suite

## Database Schema

Using SQLAlchemy with SQLite, the following tables are implemented:

- `users`: User profiles and birth details
- `subscriptions`: Subscription tracking
- `user_events`: Event logging
- `bonus_points`: Gamification tracking
- `daily_predictions`: Prediction history

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`
5. Initialize the database:
   ```bash
   python3 init_db.py
   ```
6. Run the bot:
   ```bash
   python3 -m bot.main
   ```

## Testing

Run the test suite:
```bash
python3 -m pytest tests/
```

Individual service tests:
```bash
python3 test_openai_service.py
python3 test_scheduler.py
```

## Version History

### v1.0.0
- Initial release
- Complete user registration flow
- Birth chart interpretation
- Daily forecasts
- Subscription system
- Automated task scheduling
- Database integration
- OpenAI service integration
