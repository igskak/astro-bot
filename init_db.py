from bot.services.database import engine
from bot.models.models import Base

# This will create the tables in the database specified by DATABASE_URL
Base.metadata.create_all(bind=engine)
print("Database initialized and tables created.")
