import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Float, Text
import json
import uuid

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mcp_smarttrip.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    destination = Column(String)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    itinerary_json = Column(Text)   # store full itinerary as JSON
    estimated_cost = Column(Float, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_itinerary(session: AsyncSession, trip_data: dict) -> str:
    # Pass the existing trip_id to the model
    trip = Trip(
        id = trip_data.get("trip_id"), # Use the ID from the input data
        user_id = trip_data.get("user_id"),
        destination = trip_data.get("destination", ""),
        start_date = trip_data.get("start_date"),
        end_date = trip_data.get("end_date"),
        itinerary_json = json.dumps(trip_data),
        estimated_cost = trip_data.get("total_estimated_cost")
    )
    session.add(trip)
    await session.commit()
    return trip.id

async def get_trip(session: AsyncSession, trip_id: str):
    return await session.get(Trip, trip_id)
