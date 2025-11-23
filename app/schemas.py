# filename: app/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Input Schema ---
class UserQuery(BaseModel):
    user_id: Optional[str] = None
    query: str
    preferences: Optional[dict] = None

# --- Schemas for Real-Time Data (from MCP Servers) ---
# This schema MUST match your flight_server.py
class Flight(BaseModel):
    airline: str
    flightNumber: str
    stops: int
    departure: str
    arrival: str
    duration: str
    seats: int
    price: float

# This schema MUST match your hotel_server.py
class Hotel(BaseModel):
    name: str
    rating: float
    reviews: int
    distance: str
    amenities: list[str]
    pricePerNight: float

# This schema MUST match your train_server.py
class Train(BaseModel):
    trainName: str
    trainNumber: str
    stops: int
    departure: str
    arrival: str
    duration: str
    seats: int
    price: float

# --- Schemas for AI-Generated Itinerary ---
class Activity(BaseModel):
    time: Optional[str]
    description: str

class DayPlan(BaseModel):
    day_number: int
    summary: Optional[str]
    activities: List[Activity] = []

class Itinerary(BaseModel):
    plan_name: str
    destination: str
    start_date: Optional[str]
    end_date: Optional[str]
    total_estimated_cost: float
    # These are updated to use the new MCP server models
    chosen_flight: Optional[Flight] = None
    chosen_hotel: Optional[Hotel] = None
    chosen_train: Optional[Train] = None
    days: List[DayPlan] = []

# --- Top-level Schema for the Final API Response ---
class GeneratedPlans(BaseModel):
    plans: List[Itinerary]