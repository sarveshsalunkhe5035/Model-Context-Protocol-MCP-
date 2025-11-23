# from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel
# import random
# import datetime
# import uvicorn

# # Initialized without host/port here, we'll do it in uvicorn.run
# mcp = FastMCP("Flight Server")

# class Flight(BaseModel):
#     airline: str
#     flightNumber: str
#     stops: int
#     departure: str
#     arrival: str
#     duration: str
#     seats: int
#     price: float

# class FlightSearchRequest(BaseModel):
#     destination: str
#     startDate: str
#     travelers: int

# AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]
# DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

# def create_mock_flight(destination: str, date_str: str, index: int) -> Flight:
#     airline = random.choice(AIRLINES)
#     price = random.randint(3000, 8000) * (index + 1) * 0.5
#     stops = random.choice([0, 1, 1, 2])
#     duration_hours = random.randint(1, 4) + stops
#     duration_mins = random.randint(0, 59)
#     start_time = datetime.time(random.randint(5, 20), random.randint(0, 59))
#     try: base_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError: base_date = datetime.date.today()
#     start_dt = datetime.datetime.combine(base_date, start_time)
#     end_dt = start_dt + datetime.timedelta(hours=duration_hours, minutes=duration_mins)
#     return Flight(
#         airline=airline, flightNumber=f"{airline[:2].upper()}{random.randint(100, 999)}",
#         stops=stops, departure=start_dt.isoformat(), arrival=end_dt.isoformat(),
#         duration=f"{duration_hours}h {duration_mins}m", seats=random.randint(1, 25), price=price
#     )

# @mcp.tool()
# def search_flights(request: FlightSearchRequest) -> list[Flight]:
#     print(f"[FlightServer] Searching for {request.destination}")
#     if request.destination not in DESTINATIONS: return []
#     mock_flights = [create_mock_flight(request.destination, request.startDate, i) for i in range(3)]
#     for f in mock_flights: f.price = round(f.price * request.travelers, 2)
#     return mock_flights

# if __name__ == "__main__":
#     print("Starting Flight Server on port 9001...")
#     uvicorn.run(mcp.sse_app, host="127.0.0.1", port=9001)

# filename: flight_server.py
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from pydantic import BaseModel
import random
import datetime
import uvicorn

# 1. Create a standard FastAPI app
app = FastAPI()

# 2. Initialize MCP (we keep this for project compliance)
mcp = FastMCP("Flight Server")

class Flight(BaseModel):
    airline: str
    flightNumber: str
    stops: int
    departure: str
    arrival: str
    duration: str
    seats: int
    price: float

class FlightSearchRequest(BaseModel):
    destination: str
    startDate: str
    travelers: int

AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]
DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

def create_mock_flight(destination: str, date_str: str, index: int) -> Flight:
    airline = random.choice(AIRLINES)
    price = random.randint(3000, 8000) * (index + 1) * 0.5
    stops = random.choice([0, 1, 1, 2])
    duration_hours = random.randint(1, 4) + stops
    duration_mins = random.randint(0, 59)
    start_time = datetime.time(random.randint(5, 20), random.randint(0, 59))
    try: base_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError: base_date = datetime.date.today()
    start_dt = datetime.datetime.combine(base_date, start_time)
    end_dt = start_dt + datetime.timedelta(hours=duration_hours, minutes=duration_mins)
    
    return Flight(
        airline=airline, 
        flightNumber=f"{airline[:2].upper()}{random.randint(100, 999)}",
        stops=stops, 
        departure=start_dt.isoformat(), 
        arrival=end_dt.isoformat(),
        duration=f"{duration_hours}h {duration_mins}m", 
        seats=random.randint(1, 25), 
        price=round(price, 2)
    )

# 3. Define the Logic Function
@mcp.tool()
def search_flights(request: FlightSearchRequest) -> list[Flight]:
    print(f"[FlightServer] Searching for {request.destination}")
    if request.destination not in DESTINATIONS: return []
    
    mock_flights = [create_mock_flight(request.destination, request.startDate, i) for i in range(3)]
    for f in mock_flights: 
        f.price = round(f.price * request.travelers, 2)
    return mock_flights

# 4. Add the HTTP Route to the FastAPI app
@app.post("/search_flights")
async def http_search_flights(request: FlightSearchRequest):
    return search_flights(request)

if __name__ == "__main__":
    print("Starting Flight Server on port 9001...")
    # Run 'app', not 'mcp.sse_app'
    uvicorn.run(app, host="127.0.0.1", port=9001)