# bot/main.py
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, LabeledPrice, PreCheckoutQuery
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, PreCheckoutQueryHandler
from bot.services.database import SessionLocal
from bot.models.models import User
from bot.services.openai_service import generate_natal_chart_description
from datetime import datetime

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

# Define a subscription price (in cents). Let's say $5 for a month.
MONTHLY_PRICE = LabeledPrice("Monthly Subscription", 500)  # 500 cents = $5

# Conversation states
ASK_NAME, ASK_BIRTHDATE, ASK_BIRTHTIME, ASK_BIRTHPLACE = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Check if user exists in DB
    session = SessionLocal()
    existing_user = session.query(User).filter_by(telegram_id=str(user_id)).first()

    if existing_user:
        # User is already registered
        await update.message.reply_text(
            f"Welcome back, {existing_user.name}! You can use /daily to get your daily forecast."
        )
    else:
        # Start registration process
        await update.message.reply_text(
            "Hello! I will guide you through setting up your natal chart. Let's begin.\n"
            "What's your name?"
        )
        return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Store the user's name in the context
    context.user_data["name"] = update.message.text.strip()
    await update.message.reply_text(
        "Great! Now, please provide your birthdate in YYYY-MM-DD format (e.g. 1990-04-15)."
    )
    return ASK_BIRTHDATE

async def ask_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Validate and store birthdate
    birthdate = update.message.text.strip()

    # (For simplicity, we won't do extensive validation here, but ideally you should.)
    context.user_data["birthdate"] = birthdate
    await update.message.reply_text("Got it. Please provide your birth time in HH:MM format (e.g. 14:30).")
    return ASK_BIRTHTIME

async def ask_birthtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthtime = update.message.text.strip()
    context.user_data["birthtime"] = birthtime
    await update.message.reply_text("Finally, please tell me your birthplace (e.g. New York, USA).")
    return ASK_BIRTHPLACE

async def ask_birthplace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthplace = update.message.text.strip()
    context.user_data["birthplace"] = birthplace

    # Now we have all data, let's store in DB and generate natal chart
    session = SessionLocal()
    user_id = str(update.effective_user.id)

    # Convert birthdate string to Python date object
    birthdate = datetime.strptime(context.user_data["birthdate"], "%Y-%m-%d").date()

    # Create and save user in DB
    new_user = User(
        telegram_id=user_id,
        name=context.user_data["name"],
        birthdate=birthdate,  # Now passing a proper date object
        birthtime=context.user_data["birthtime"],
        birthplace=context.user_data["birthplace"]
    )
    session.add(new_user)
    session.commit()

    # Generate natal chart description
    natal_desc = generate_natal_chart_description(
        name=new_user.name,
        birthdate=new_user.birthdate.isoformat(),
        birthtime=new_user.birthtime,
        birthplace=new_user.birthplace
    )

    # Send natal chart description to user
    await update.message.reply_text("Thank you! Here's your natal chart interpretation:")
    await update.message.reply_text(natal_desc)

    await update.message.reply_text("You are all set! From now on, you can use /daily to get your daily forecast.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def daily_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = str(update.effective_user.id)
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()

    if not user:
        await update.message.reply_text("I don't have your details yet. Please use /start to register.")
        return

    from bot.services.subscription_service import is_subscription_active
    if not is_subscription_active(user_id):
        await update.message.reply_text("You need an active subscription to view the daily forecast. Use /subscribe to get one!")
        return

    # If subscription is active, proceed
    from bot.services.openai_service import generate_daily_prediction
    forecast = generate_daily_prediction(user.name)
    await update.message.reply_text(forecast)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # If user already has an active subscription, inform them
    from bot.services.subscription_service import is_subscription_active
    if is_subscription_active(user_id):
        await update.message.reply_text("You already have an active subscription!")
        return

    # Send an invoice
    await update.message.reply_invoice(
        title="Monthly Astrological Subscription",
        description="Access to daily personalized forecasts and advanced features for a month.",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="USD",
        prices=[MONTHLY_PRICE],
        start_parameter="astro-subscription",
        payload="monthly_sub"
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    # You can perform some checks here if necessary.
    await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Create or renew subscription after successful payment
    from bot.services.subscription_service import create_or_renew_subscription
    create_or_renew_subscription(user_id, days=30)  # 30 days subscription

    await update.message.reply_text("Thank you for your purchase! Your subscription is now active.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birthdate)],
            ASK_BIRTHTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birthtime)],
            ASK_BIRTHPLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birthplace)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("daily", daily_forecast))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
