# bot/services/subscription_service.py
from datetime import date, timedelta
from bot.services.database import SessionLocal
from bot.models.models import Subscription, User

def get_current_subscription(user_id: str) -> Subscription:
    session = SessionLocal()
    sub = session.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active'
    ).order_by(Subscription.end_date.desc()).first()
    session.close()
    return sub

def create_or_renew_subscription(user_id: str, days=30, sub_type='basic'):
    session = SessionLocal()
    existing_sub = get_current_subscription(user_id)
    if existing_sub:
        # Extend current subscription
        existing_sub.end_date += timedelta(days=days)
    else:
        # Create a new subscription
        new_sub = Subscription(
            user_id=user_id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=days),
            status='active',
            type=sub_type
        )
        session.add(new_sub)
    session.commit()
    session.close()

def is_subscription_active(user_id: str) -> bool:
    sub = get_current_subscription(user_id)
    if not sub:
        return False
    # Check if end_date is still in the future
    return sub.end_date >= date.today()