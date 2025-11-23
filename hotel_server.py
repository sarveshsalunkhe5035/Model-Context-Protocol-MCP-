# from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel
# import random
# import uvicorn

# mcp = FastMCP("Hotel Server")

# class Hotel(BaseModel):
#     name: str
#     rating: float
#     reviews: int
#     distance: str
#     amenities: list[str]
#     pricePerNight: float

# class HotelSearchRequest(BaseModel):
#     destination: str
#     startDate: str
#     endDate: str
#     travelers: int
#     accommodationType: str

# HOTEL_NAMES = {
#     "Jaipur": ["The Raj Palace", "Samode Haveli", "Rambagh Palace"],
#     "Goa": ["Taj Exotica", "W Goa", "Goa Marriott Resort"],
#     "Kerala": ["Kumarakom Lake Resort", "Brunton Boatyard", "Spice Village"],
#     "Manali": ["The Himalayan", "Manuallaya Resort", "Snow Valley Resorts"],
#     "Default": ["Generic Hotel", "City Inn", "Travelers Lodge"]
# }
# AMENITIES = ["Wifi", "Pool", "Free Breakfast", "Gym", "Parking", "Spa"]
# DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

# def create_mock_hotel(destination: str, index: int) -> Hotel:
#     names = HOTEL_NAMES.get(destination, HOTEL_NAMES["Default"])
#     name = names[index % len(names)]
#     if index == 0: rating, price = round(random.uniform(3.0, 4.0), 1), random.randint(1500, 3000)
#     elif index == 1: rating, price = round(random.uniform(4.0, 4.7), 1), random.randint(3500, 6000)
#     else: rating, price = round(random.uniform(4.5, 5.0), 1), random.randint(7000, 15000)
#     return Hotel(
#         name=f"{name} {destination}", rating=rating, reviews=random.randint(50, 1000),
#         distance=f"{round(random.uniform(0.5, 5.0), 1)}km center",
#         amenities=random.sample(AMENITIES, k=random.randint(3, 6)), pricePerNight=float(price)
#     )

# @mcp.tool()
# def search_hotels(request: HotelSearchRequest) -> list[Hotel]:
#     print(f"[HotelServer] Searching in {request.destination}")
#     if request.destination not in DESTINATIONS: return []
#     mock_hotels = [create_mock_hotel(request.destination, i) for i in range(3)]
#     rooms = (request.travelers + 1) // 2
#     for h in mock_hotels: h.pricePerNight = round(h.pricePerNight * rooms, 2)
#     return mock_hotels

# if __name__ == "__main__":
#     print("Starting Hotel Server on port 9002...")
#     uvicorn.run(mcp.sse_app, host="127.0.0.1", port=9002)

# filename: hotel_server.py
# filename: hotel_server.py
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()
mcp = FastMCP("Hotel Server")

class Hotel(BaseModel):
    name: str
    rating: float
    reviews: int
    distance: str
    amenities: list[str]
    pricePerNight: float

class HotelSearchRequest(BaseModel):
    destination: str
    startDate: str
    endDate: str
    travelers: int
    accommodationType: str

HOTEL_NAMES = {
    "Jaipur": ["The Raj Palace", "Samode Haveli", "Rambagh Palace"],
    "Goa": ["Taj Exotica", "W Goa", "Goa Marriott Resort"],
    "Kerala": ["Kumarakom Lake Resort", "Brunton Boatyard", "Spice Village"],
    "Manali": ["The Himalayan", "Manuallaya Resort", "Snow Valley Resorts"],
    "Default": ["Generic Hotel", "City Inn", "Travelers Lodge"]
}
AMENITIES = ["Wifi", "Pool", "Free Breakfast", "Gym", "Parking", "Spa"]
DESTINATIONS = ["Jaipur", "Goa", "Kerala", "Manali", "Agra", "Delhi", "Mumbai", "Bangalore"]

def create_mock_hotel(destination: str, index: int) -> Hotel:
    names = HOTEL_NAMES.get(destination, HOTEL_NAMES["Default"])
    name = names[index % len(names)]
    if index == 0: rating, price = round(random.uniform(3.0, 4.0), 1), random.randint(1500, 3000)
    elif index == 1: rating, price = round(random.uniform(4.0, 4.7), 1), random.randint(3500, 6000)
    else: rating, price = round(random.uniform(4.5, 5.0), 1), random.randint(7000, 15000)
    
    return Hotel(
        name=f"{name} {destination}", 
        rating=rating, 
        reviews=random.randint(50, 1000),
        distance=f"{round(random.uniform(0.5, 5.0), 1)}km center",
        amenities=random.sample(AMENITIES, k=random.randint(3, 6)), 
        pricePerNight=float(price)
    )

@mcp.tool()
def search_hotels(request: HotelSearchRequest) -> list[Hotel]:
    print(f"[HotelServer] Searching in {request.destination}")
    if request.destination not in DESTINATIONS: return []
    
    mock_hotels = [create_mock_hotel(request.destination, i) for i in range(3)]
    rooms = (request.travelers + 1) // 2
    for h in mock_hotels: 
        h.pricePerNight = round(h.pricePerNight * rooms, 2)
    return mock_hotels

@app.post("/search_hotels")
async def http_search_hotels(request: HotelSearchRequest):
    return search_hotels(request)

if __name__ == "__main__":
    print("Starting Hotel Server on port 9002...")
    uvicorn.run(app, host="127.0.0.1", port=9002)