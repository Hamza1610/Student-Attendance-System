from app.models.attendance_model import Base  # Import your Base model
from app.db.base import engine  # Import your engine

# Drop and recreate tables
with engine.begin() as conn:
    Base.metadata.drop_all(bind=conn)  # Drop all tables
    Base.metadata.create_all(bind=conn)  # Recreate tables
