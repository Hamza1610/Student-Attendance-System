from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# # Create the async engine (provide your database URL here)
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
# engine = create_async_engine(DATABASE_URL, echo=True)

# # Create sessionmaker for async sessions
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )
