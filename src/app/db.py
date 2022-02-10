import os

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Float,
    Table,
    create_engine
)
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


weather = Table(
    "weather",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("temperature", Float),
    Column("headers", String(500)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
    Column("updated_date", DateTime, default=func.now(), nullable=False),

)

# databases query builder
database = Database(DATABASE_URL)
