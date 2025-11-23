# from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel
# import random
# import datetime
# import uvicorn

# mcp = FastMCP("Train Server")

# class Train(BaseModel):
#     trainName: str
#     trainNumber: str
#     stops: int
#     departure: str
#     arrival: str
#     duration: str
#     seats: int
#     price: float

# class TrainSearchRequest(BaseModel):
#     destination: str
#     startDate: str
#     travelers: int

# TRAIN_NAMES = ["Shatabdi Express", "Rajdhani Express", "Duronto Express", "Vande Bharat"]
# DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

# def create_mock_train(destination: str, date_str: str, index: int) -> Train:
#     name = random.choice(TRAIN_NAMES)
#     price = [random.randint(500, 1200), random.randint(1500, 2500), random.randint(3000, 5000)][index]
#     duration_hours, duration_mins = random.randint(6, 24), random.randint(0, 59)
#     start_time = datetime.time(random.randint(5, 20), random.randint(0, 59))
#     try: base_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError: base_date = datetime.date.today()
#     start_dt = datetime.datetime.combine(base_date, start_time)
#     end_dt = start_dt + datetime.timedelta(hours=duration_hours, minutes=duration_mins)
#     return Train(
#         trainName=name, trainNumber=str(random.randint(12000, 12999)), stops=random.randint(5, 15),
#         departure=start_dt.isoformat(), arrival=end_dt.isoformat(),
#         duration=f"{duration_hours}h {duration_mins}m", seats=random.randint(10, 100), price=float(price)
#     )

# @mcp.tool()
# def search_trains(request: TrainSearchRequest) -> list[Train]:
#     print(f"[TrainServer] Searching for {request.destination}")
#     if request.destination not in DESTINATIONS: return []
#     mock_trains = [create_mock_train(request.destination, request.startDate, i) for i in range(3)]
#     for t in mock_trains: t.price = round(t.price * request.travelers, 2)
#     return mock_trains

# if __name__ == "__main__":
#     print("Starting Train Server on port 9003...")
#     uvicorn.run(mcp.sse_app, host="127.0.0.1", port=9003)

# filename: train_server.py
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from pydantic import BaseModel
import random
import datetime
import uvicorn

app = FastAPI()
mcp = FastMCP("Train Server")

class Train(BaseModel):
    trainName: str
    trainNumber: str
    stops: int
    departure: str
    arrival: str
    duration: str
    seats: int
    price: float

class TrainSearchRequest(BaseModel):
    destination: str
    startDate: str
    travelers: int

TRAIN_NAMES = ["Shatabdi Express", "Rajdhani Express", "Duronto Express", "Vande Bharat"]
DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

def create_mock_train(destination: str, date_str: str, index: int) -> Train:
    name = random.choice(TRAIN_NAMES)
    price = [random.randint(500, 1200), random.randint(1500, 2500), random.randint(3000, 5000)][index]
    duration_hours, duration_mins = random.randint(6, 24), random.randint(0, 59)
    start_time = datetime.time(random.randint(5, 20), random.randint(0, 59))
    try: base_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError: base_date = datetime.date.today()
    start_dt = datetime.datetime.combine(base_date, start_time)
    end_dt = start_dt + datetime.timedelta(hours=duration_hours, minutes=duration_mins)
    
    return Train(
        trainName=name, 
        trainNumber=str(random.randint(12000, 12999)), 
        stops=random.randint(5, 15),
        departure=start_dt.isoformat(), 
        arrival=end_dt.isoformat(),
        duration=f"{duration_hours}h {duration_mins}m", 
        seats=random.randint(10, 100), 
        price=float(price)
    )

@mcp.tool()
def search_trains(request: TrainSearchRequest) -> list[Train]:
    print(f"[TrainServer] Searching for {request.destination}")
    if request.destination not in DESTINATIONS: return []
    
    mock_trains = [create_mock_train(request.destination, request.startDate, i) for i in range(3)]
    for t in mock_trains: 
        t.price = round(t.price * request.travelers, 2)
    return mock_trains

@app.post("/search_trains")
async def http_search_trains(request: TrainSearchRequest):
    return search_trains(request)

if __name__ == "__main__":
    print("Starting Train Server on port 9003...")
    uvicorn.run(app, host="127.0.0.1", port=9003)