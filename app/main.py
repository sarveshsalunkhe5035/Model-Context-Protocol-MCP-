# # filename: app/main.py

# import logging
# import json
# import asyncio
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# load_dotenv()

# # We import the NEW schemas and gateway functions
# from app.schemas import UserQuery, Itinerary, GeneratedPlans
# from app.gemini_client import GeminiClient
# from app.storage import AsyncSessionLocal, init_db, get_trip
# from app.travel_gateways import search_flights, search_hotels, search_trains

# app = FastAPI(title="MCP Smart Trip - MCP Server")

# # --- CORS Middleware ---
# origins = ["http://localhost", "http://localhost:8080", "http://127.0.0.1:5500", "null"]
# app.add_middleware(
#     CORSMiddleware, allow_origins=origins, allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# # --- Logging and Client Setup ---
# logger = logging.getLogger("mcp_server")
# logging.basicConfig(level=logging.INFO)
# gemini = GeminiClient()
# # gemini = GeminiClient(model="gemini-2.5-pro")
# logger.info("Gemini client initialized.")

# # --- Database Dependency ---
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

# @app.on_event("startup")
# async def startup():
#     await init_db()
#     logger.info("Database initialized.")

# # --- API Endpoints ---
# @app.post("/api/query", response_model=GeneratedPlans)
# async def handle_query(q: UserQuery, db=Depends(get_db)):
#     try:
#         # --- Extract structured data (same as before) ---
#         query_lower = q.query.lower()
#         if "goa" in query_lower: destination = "Goa"
#         elif "delhi" in query_lower: destination = "Delhi"
#         elif "jaipur" in query_lower: destination = "Jaipur"
#         elif "manali" in query_lower: destination = "Manali"
#         else: destination = "Mumbai" # Default fallback

#         # --- Define parameters for the MCP search requests ---
#         start_date = "2026-05-10"
#         end_date = "2026-05-15"
#         travelers = 2
#         accommodation_type = "Hotel" # Example default

#         # --- Build the request dictionaries for our MCP servers ---
#         flight_request = {
#             "destination": destination,
#             "startDate": start_date,
#             "travelers": travelers
#         }
#         hotel_request = {
#             "destination": destination,
#             "startDate": start_date,
#             "endDate": end_date,
#             "travelers": travelers,
#             "accommodationType": accommodation_type
#         }
#         train_request = {
#             "destination": destination,
#             "startDate": start_date,
#             "travelers": travelers
#         }
        
#         # --- The New Orchestration Flow (using MCP) ---
#         logger.info(f"Fetching data from MCP servers for: {destination}")
        
#         # Create tasks to call the new gateway functions
#         flights_task = search_flights(flight_request)
#         hotels_task = search_hotels(hotel_request)
#         trains_task = search_trains(train_request)

#         flights, hotels, trains = await asyncio.gather(flights_task, hotels_task, trains_task)
#         logger.info(f"Got {len(flights)} flights, {len(hotels)} hotels, {len(trains)} trains.")

#         # --- Call Gemini (this part is unchanged) ---
#         gemini_output = await gemini.generate_itineraries(q.query, destination, flights, hotels, trains)

#         if "plans" not in gemini_output or not isinstance(gemini_output["plans"], list):
#             logger.error(f"AI failed to generate valid plans. Output: {gemini_output}")
#             raise HTTPException(status_code=500, detail="AI failed to generate valid plans.")

#         logger.info(f"Successfully generated {len(gemini_output['plans'])} plans.")
#         return gemini_output

#     except Exception as e:
#         logger.exception("Error handling query")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/trip/{trip_id}", response_model=Itinerary)
# async def get_trip_endpoint(trip_id: str, db=Depends(get_db)):
#     t = await get_trip(db, trip_id)
#     if not t:
#         raise HTTPException(status_code=404, detail="Trip not found")
#     return json.loads(t.itinerary_json)

# filename: app/main.py

import logging
import json
import asyncio
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# We import the NEW schemas and gateway functions
from app.schemas import UserQuery, Itinerary, GeneratedPlans
from app.gemini_client import GeminiClient
from app.storage import AsyncSessionLocal, init_db, get_trip
from app.travel_gateways import search_flights, search_hotels, search_trains

app = FastAPI(title="MCP Smart Trip - MCP Server")

# --- CORS Middleware ---
origins = ["http://localhost", "http://localhost:8080", "http://127.0.0.1:5500", "null"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# --- Logging and Client Setup ---
logger = logging.getLogger("mcp_server")
logging.basicConfig(level=logging.INFO)

# UPDATED: We initialize GeminiClient without arguments, so it uses DEFAULT_MODEL (gemini-2.5-flash)
gemini = GeminiClient()
logger.info(f"Gemini client initialized with model: {gemini.model}")

# --- Database Dependency ---
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    await init_db()
    logger.info("Database initialized.")

# --- API Endpoints ---
@app.post("/api/query", response_model=GeneratedPlans)
async def handle_query(q: UserQuery, db=Depends(get_db)):
    try:
        query_lower = q.query.lower()
        if "goa" in query_lower: destination = "Goa"
        elif "delhi" in query_lower: destination = "Delhi"
        elif "jaipur" in query_lower: destination = "Jaipur"
        elif "manali" in query_lower: destination = "Manali"
        else: destination = "Mumbai" 

        start_date = "2026-05-10"
        end_date = "2026-05-15"
        travelers = 2
        accommodation_type = "Hotel" 

        flight_request = {
            "destination": destination,
            "startDate": start_date,
            "travelers": travelers
        }
        hotel_request = {
            "destination": destination,
            "startDate": start_date,
            "endDate": end_date,
            "travelers": travelers,
            "accommodationType": accommodation_type
        }
        train_request = {
            "destination": destination,
            "startDate": start_date,
            "travelers": travelers
        }
        
        logger.info(f"Fetching data from MCP servers for: {destination}")
        
        flights_task = search_flights(flight_request)
        hotels_task = search_hotels(hotel_request)
        trains_task = search_trains(train_request)

        flights, hotels, trains = await asyncio.gather(flights_task, hotels_task, trains_task)
        logger.info(f"Got {len(flights)} flights, {len(hotels)} hotels, {len(trains)} trains.")

        # Call Gemini
        gemini_output = await gemini.generate_itineraries(q.query, destination, flights, hotels, trains)

        if "plans" not in gemini_output or not isinstance(gemini_output["plans"], list):
            logger.error(f"AI failed to generate valid plans. Output: {gemini_output}")
            raise HTTPException(status_code=500, detail="AI failed to generate valid plans.")

        logger.info(f"Successfully generated {len(gemini_output['plans'])} plans.")
        return gemini_output

    except Exception as e:
        logger.exception("Error handling query")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trip/{trip_id}", response_model=Itinerary)
async def get_trip_endpoint(trip_id: str, db=Depends(get_db)):
    t = await get_trip(db, trip_id)
    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")
    return json.loads(t.itinerary_json)