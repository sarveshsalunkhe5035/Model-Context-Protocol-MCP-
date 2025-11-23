# import os
# import logging
# import httpx
# import json
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from typing import List, Dict

# # --- Constants and Configuration ---
# GEMINI_API_URL = os.getenv("GEMINI_API_URL")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# logger = logging.getLogger("gemini_client")
# HEADERS = { "Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY }

# # --- Helper Function for API Calls ---
# @retry(
#     reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10),
#     retry=retry_if_exception_type((httpx.HTTPError,))
# )
# async def _post_with_retry(payload: dict):
#     """Makes a POST request to the Gemini API with exponential backoff retry logic."""
#     async with httpx.AsyncClient(timeout=120.0) as client:
#         resp = await client.post(GEMINI_API_URL, json=payload, headers=HEADERS)
#         resp.raise_for_status()
#         return resp.json()

# # --- Gemini Client Class with Upgraded Logic ---
# class GeminiClient:
#     def __init__(self, model: str = "gemini-2.5-pro"):
#         self.model = model

#     async def generate_itineraries(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> dict:
#         """
#         Generates multiple itinerary options by providing real-time data (flights, hotels)
#         as context to the Gemini model.
#         """
#         prompt = self._build_grounded_prompt(user_query, destination, flights, hotels, trains)
#         payload = {
#             "contents": [{"parts": [{"text": prompt}]}],
#             "generationConfig": {
#                 "temperature": 0.5,
#                 "maxOutputTokens": 8192,
#                 "responseMimeType": "application/json",
#             },
#         }
#         logger.info("Sending grounded request to Gemini...")
#         result = await _post_with_retry(payload)
#         logger.info(f"Gemini raw response: {json.dumps(result, indent=2)}")
#         return self._parse_gemini_result(result)

#     def _build_grounded_prompt(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> str:
#         """
#         Constructs a detailed, structured prompt to guide the AI, grounding it with
#         real-time data and enforcing a strict JSON output format.
#         """
#         # Convert the real-time data into a string format for the prompt
#         flights_text = json.dumps(flights) if flights else "not available"
#         hotels_text = json.dumps(hotels) if hotels else "not available"
#         trains_text = json.dumps(trains) if trains else "not available"

#         # This is the new, highly detailed prompt engineering
#         prompt = (
#             "You are an expert Indian travel agent. Your task is to create a set of distinct travel plans based on a user's request and a catalog of real-time data.\n\n"
#             f"**User's Request:** \"{user_query}\"\n"
#             f"**Destination:** \"{destination}\"\n\n"
#             "**Real-time Data Catalog (You MUST use this data to build the plans):**\n"
#             f"- Available Flights: {flights_text}\n"
#             f"- Available Hotels: {hotels_text}\n"
#             f"- Available Trains: {trains_text}\n\n"
#             "**Your Task & Instructions:**\n"
#             "1. Create 2-3 distinct itinerary options (e.g., budget, luxury, balanced) based on the user's request and the data catalog.\n"
#             "2. For EACH itinerary, you MUST select ONE flight (if relevant) and ONE hotel from the provided data catalog.\n"
#             "3. **JSON STRUCTURE IS CRITICAL:** Your response MUST be a single raw JSON object with one key: `plans`. The `plans` key must contain an array of itinerary objects.\n"
#             "4. Each itinerary object in the array MUST contain the following keys:\n"
#             "   - `plan_name`: A descriptive name (e.g., 'Budget Goa Getaway').\n"
#             f"   - `destination`: This MUST be '{destination}'.\n"
#             "   - `start_date`, `end_date`: Infer from the query if possible, otherwise use null.\n"
#             "   - `total_estimated_cost`: Accurately calculated total cost for the whole trip.\n"
#             "   - `chosen_flight`, `chosen_hotel`, `chosen_train`: The full JSON object for the item you selected from the catalog. Use null if not applicable.\n"
#             "   - `days`: An array of `DayPlan` objects. **The key MUST be `days`**.\n"
#             "5. Each object inside the `days` array must contain:\n"
#             "   - `day_number`: The day number (integer).\n"
#             "   - `summary`: A brief summary for the day.\n"
#             "   - `activities`: An array of `Activity` objects. Each activity object must have a `description` (string) and `time` (string).\n"
#             "Adhere strictly to this structure. Do NOT include any extra text, explanations, or markdown formatting outside of the main JSON object."
#         )
#         return prompt

#     def _parse_gemini_result(self, raw_json: dict) -> dict:
#         """Parses the JSON response from Gemini, expecting a specific structure."""
#         try:
#             # Directly access the text from the expected response structure
#             text_content = raw_json["candidates"][0]["content"]["parts"][0]["text"]
#             return json.loads(text_content)
#         except (KeyError, IndexError, json.JSONDecodeError) as e:
#             logger.error(f"Could not parse Gemini response: {e}")
#             logger.error(f"Raw JSON received: {raw_json}")
#             # Return a structured error that the frontend can display
#             return {"error": "Failed to parse AI response.", "details": str(raw_json)}

# import os
# import logging
# import httpx
# import json
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from typing import List, Dict

# # --- Constants and Configuration ---
# GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# logger = logging.getLogger("gemini_client")
# HEADERS = { "Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY }

# # --- Helper Function for API Calls ---
# @retry(
#     reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10),
#     retry=retry_if_exception_type((httpx.HTTPError,))
# )
# async def _post_with_retry(payload: dict):
#     """Makes a POST request to the Gemini API with exponential backoff retry logic."""
#     async with httpx.AsyncClient(timeout=120.0) as client:
#         resp = await client.post(GEMINI_API_URL, json=payload, headers=HEADERS)
#         resp.raise_for_status()
#         return resp.json()

# # --- Gemini Client Class with Upgraded Logic ---
# class GeminiClient:
#     def __init__(self, model: str = "gemini-2.5-pro"):
#         self.model = model
#         if not GEMINI_API_KEY:
#             logger.warning("GEMINI_API_KEY environment variable not set. API calls will fail.")
#         if "generateContent" not in GEMINI_API_URL:
#             logger.warning(f"GEMINI_API_URL seems incorrect. Should end with :generateContent. Current value: {GEMINI_API_URL}")

#     async def generate_itineraries(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> dict:
#         """
#         Generates multiple itinerary options by providing real-time data (flights, hotels)
#         as context to the Gemini model.
#         """
#         # This is the line we are changing
#         prompt = self._build_grounded_prompt(user_query, destination, flights, hotels, trains)
#         payload = {
#             "contents": [{"parts": [{"text": prompt}]}],
#             "generationConfig": {
#                 "temperature": 0.5,
#                 "maxOutputTokens": 8192,
#                 "responseMimeType": "application/json",
#             },
#         }
#         logger.info("Sending grounded request to Gemini...")
#         result = await _post_with_retry(payload)
#         logger.info(f"Gemini raw response: {json.dumps(result, indent=2)}")
#         return self._parse_gemini_result(result)

#     def _build_grounded_prompt(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> str:
#         """
#         Constructs a detailed, structured prompt to guide the AI, grounding it with
#         real-time data and enforcing a strict JSON output format.
#         """
#         flights_text = json.dumps(flights) if flights else "not available"
#         hotels_text = json.dumps(hotels) if hotels else "not available"
#         trains_text = json.dumps(trains) if trains else "not available"

#         # This is the new, highly detailed prompt engineering
#         prompt = (
#             "You are an expert Indian travel agent. Your task is to create a set of distinct travel plans based on a user's request and a catalog of real-time data.\n\n"
#             f"**User's Request:** \"{user_query}\"\n"
#             f"**Destination:** \"{destination}\"\n\n"
#             "**Real-time Data Catalog (You MUST use this data to build the plans):**\n"
#             f"- Available Flights: {flights_text}\n"
#             f"- Available Hotels: {hotels_text}\n"
#             f"- Available Trains: {trains_text}\n\n"
#             "**Your Task & Instructions (VERY IMPORTANT):**\n"
#             "1. Create 2-3 distinct itinerary options (e.g., budget, luxury, balanced) based on the user's request and the data catalog.\n"
#             "2. **CRITICAL:** For EACH itinerary, you MUST select one flight, one hotel, and/or one train *directly* from the data catalogs provided above.\n"
#             "3. **DO NOT INVENT or MODIFY data.** The `chosen_flight`, `chosen_hotel`, and `chosen_train` objects in your JSON response **MUST BE an exact, 1-to-1 copy-paste** of one of the JSON objects from the 'Available Flights', 'Available Hotels', or 'Available Trains' data. Do not add, remove, or rename any fields.\n"
#             "4. **JSON STRUCTURE IS CRITICAL:** Your response MUST be a single raw JSON object with one key: `plans`. The `plans` key must contain an array of itinerary objects.\n"
#             "5. Each itinerary object in the array MUST contain the following keys:\n"
#             "   - `plan_name`: A descriptive name (e.g., 'Budget Goa Getaway').\n"
#             f"   - `destination`: This MUST be '{destination}'.\n"
#             "   - `start_date`, `end_date`: Infer from the query if possible, otherwise use null.\n"
#             "   - `total_estimated_cost`: Accurately calculated total cost for the whole trip.\n"
#             "   - `chosen_flight`, `chosen_hotel`, `chosen_train`: The **exact JSON object** you copy-pasted from the catalog. Use `null` if not applicable.\n"
#             "   - `days`: An array of `DayPlan` objects. **The key MUST be `days`**.\n"
#             "6. Each object inside the `days` array must contain:\n"
#             "   - `day_number`: The day number (integer).\n"
#             "   - `summary`: A brief summary for the day.\n"
#             "   - `activities`: An array of `Activity` objects. Each activity object must have a `description` (string) and `time` (string).\n"
#             "Adhere strictly to this structure. Do NOT include any extra text, explanations, or markdown formatting outside of the main JSON object."
#         )
#         return prompt

#     def _parse_gemini_result(self, raw_json: dict) -> dict:
#         """Parses the JSON response from Gemini, expecting a specific structure."""
#         try:
#             # Directly access the text from the expected response structure
#             text_content = raw_json["candidates"][0]["content"]["parts"][0]["text"]
#             # Clean the text in case Gemini wraps it in markdown
#             if text_content.startswith("```json"):
#                 text_content = text_content[7:-3].strip() # Remove ```json and ```
#             elif text_content.startswith("```"):
#                 text_content = text_content[3:-3].strip() # Remove ``` and ```

#             return json.loads(text_content)
#         except (KeyError, IndexError, json.JSONDecodeError) as e:
#             logger.error(f"Could not parse Gemini response: {e}")
#             logger.error(f"Raw JSON received: {raw_json}")
#             # Return a structured error that the frontend can display
#             return {"error": "Failed to parse AI response.", "details": str(raw_json)}

# import os
# import logging
# import httpx
# import json
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from typing import List, Dict, Any

# # --- Constants and Configuration ---
# GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# logger = logging.getLogger("gemini_client")
# HEADERS = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

# # --- Helper Function for API Calls ---
# @retry(
#     reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10),
#     retry=retry_if_exception_type((httpx.HTTPError,))
# )
# async def _post_with_retry(payload: dict):
#     async with httpx.AsyncClient(timeout=120.0) as client:
#         resp = await client.post(GEMINI_API_URL, json=payload, headers=HEADERS)
#         resp.raise_for_status()
#         return resp.json()

# # --- Gemini Client Class with Upgraded Logic ---
# class GeminiClient:
#     def __init__(self, model: str = "gemini-2.5-pro"):
#         self.model = model
#         if not GEMINI_API_KEY:
#             logger.warning("GEMINI_API_KEY environment variable not set. API calls will fail.")
#         if "generateContent" not in GEMINI_API_URL:
#             logger.warning(f"GEMINI_API_URL seems incorrect. Should end with :generateContent. Current value: {GEMINI_API_URL}")

#     async def generate_itineraries(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> dict:
#         prompt = self._build_grounded_prompt(user_query, destination, flights, hotels, trains)
#         payload = {
#             "contents": [{"parts": [{"text": prompt}]}],
#             "generationConfig": {
#                 "temperature": 0.5,
#                 "maxOutputTokens": 8192,
#                 "responseMimeType": "application/json",
#             },
#         }
#         logger.info("Sending grounded request to Gemini...")
#         result = await _post_with_retry(payload)
#         logger.info(f"Gemini raw response: {json.dumps(result, indent=2)}")
#         return self._parse_gemini_result(result)

#     def _build_grounded_prompt(
#         self,
#         user_query: str,
#         destination: str,
#         flights: List[Dict],
#         hotels: List[Dict],
#         trains: List[Dict]
#     ) -> str:
#         flights_text = json.dumps(flights) if flights else "not available"
#         hotels_text = json.dumps(hotels) if hotels else "not available"
#         trains_text = json.dumps(trains) if trains else "not available"

#         prompt = (
#             "You are an expert Indian travel agent. Your task is to create a set of distinct travel plans based on a user's request and a catalog of real-time data.\n\n"
#             f"**User's Request:** \"{user_query}\"\n"
#             f"**Destination:** \"{destination}\"\n\n"
#             "**Real-time Data Catalog (You MUST use this data to build the plans):**\n"
#             f"- Available Flights: {flights_text}\n"
#             f"- Available Hotels: {hotels_text}\n"
#             f"- Available Trains: {trains_text}\n\n"
#             "**Your Task & Instructions (VERY IMPORTANT):**\n"
#             "1. Create 2-3 distinct itinerary options (e.g., budget, luxury, balanced) based on the user's request and the data catalog.\n"
#             "2. **CRITICAL:** For EACH itinerary, you MUST select one flight, one hotel, and/or one train *directly* from the data catalogs provided above.\n"
#             "3. **DO NOT INVENT or MODIFY data.** The `chosen_flight`, `chosen_hotel`, and `chosen_train` objects in your JSON response **MUST BE an exact, 1-to-1 copy-paste** of one of the JSON objects from the 'Available Flights', 'Available Hotels', or 'Available Trains' data. Do not add, remove, or rename any fields.\n"
#             "4. **JSON STRUCTURE IS CRITICAL:** Your response MUST be a single raw JSON object with one key: `plans`. The `plans` key must contain an array of itinerary objects.\n"
#             "5. Each itinerary object in the array MUST contain the following keys:\n"
#             "   - `plan_name`: A descriptive name (e.g., 'Budget Goa Getaway').\n"
#             f"   - `destination`: This MUST be '{destination}'.\n"
#             "   - `start_date`, `end_date`: Infer from the query if possible, otherwise use null.\n"
#             "   - `total_estimated_cost`: Accurately calculated total cost for the whole trip.\n"
#             "   - `chosen_flight`, `chosen_hotel`, `chosen_train`: The **exact JSON object** you copy-pasted from the catalog. Use `null` if not applicable.\n"
#             "   - `days`: An array of `DayPlan` objects. **The key MUST be `days`**.\n"
#             "6. Each object inside the `days` array must contain:\n"
#             "   - `day_number`: The day number (integer).\n"
#             "   - `summary`: A brief summary for the day.\n"
#             "   - `activities`: An array of `Activity` objects. Each activity object must have a `description` (string) and `time` (string).\n"
#             "Adhere strictly to this structure. Do NOT include any extra text, explanations, or markdown formatting outside of the main JSON object."
#         )
#         return prompt

#     def _parse_gemini_result(self, raw_json: dict) -> dict:
#         try:
#             text_content = raw_json["candidates"][0]["content"]["parts"][0]["text"]
#             if text_content.startswith("```json"):
#                 text_content = text_content[7:-3].strip()
#             elif text_content.startswith("```"):
#                 text_content = text_content[3:-3].strip()

#             plans = json.loads(text_content)

#             # Restructure chosen_flight, chosen_hotel, chosen_train
#             for plan in plans.get("plans", []):
#                 if isinstance(plan.get("chosen_flight"), dict) and "data" in plan["chosen_flight"]:
#                     plan["chosen_flight"] = plan["chosen_flight"]["data"]
#                 if isinstance(plan.get("chosen_hotel"), dict) and "data" in plan["chosen_hotel"]:
#                     plan["chosen_hotel"] = plan["chosen_hotel"]["data"]
#                 if isinstance(plan.get("chosen_train"), dict) and "data" in plan["chosen_train"]:
#                     plan["chosen_train"] = plan["chosen_train"]["data"]

#             return plans
#         except (KeyError, IndexError, json.JSONDecodeError) as e:
#             logger.error(f"Could not parse Gemini response: {e}")
#             logger.error(f"Raw JSON received: {raw_json}")
#             return {"error": "Failed to parse AI response.", "details": str(raw_json)}

# filename: app/gemini_client.py

# filename: app/gemini_client.py

# filename: app/gemini_client.py

import os
import logging
import httpx
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import List, Dict, Any

# --- Configuration ---
# UPDATED: Using the latest stable Flash model (Nov 2025)
DEFAULT_MODEL = "gemini-2.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

logger = logging.getLogger("gemini_client")

# --- Helper Function for API Calls ---
@retry(
    reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10),
    retry=retry_if_exception_type((httpx.HTTPError,))
)
async def _post_with_retry(url: str, payload: dict):
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    # Passing key as query param as a backup
    params = {"key": GEMINI_API_KEY}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

# --- Gemini Client Class ---
class GeminiClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        if not GEMINI_API_KEY:
            logger.error("CRITICAL: GEMINI_API_KEY is missing in .env file!")

    async def generate_itineraries(
        self,
        user_query: str,
        destination: str,
        flights: List[Dict],
        hotels: List[Dict],
        trains: List[Dict]
    ) -> dict:
        # 1. Build the Prompt
        prompt = self._build_grounded_prompt(user_query, destination, flights, hotels, trains)
        
        # 2. Construct the URL (models/gemini-2.5-flash:generateContent)
        url = f"{BASE_URL}/{self.model}:generateContent"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json",
            },
        }
        
        logger.info(f"Sending request to Gemini ({self.model})...")
        try:
            result = await _post_with_retry(url, payload)
            return self._parse_gemini_result(result)
        except httpx.HTTPStatusError as e:
            logger.error(f"Gemini API Error {e.response.status_code}: {e.response.text}")
            raise

    def _build_grounded_prompt(
        self,
        user_query: str,
        destination: str,
        flights: List[Dict],
        hotels: List[Dict],
        trains: List[Dict]
    ) -> str:
        flights_text = json.dumps(flights) if flights else "not available"
        hotels_text = json.dumps(hotels) if hotels else "not available"
        trains_text = json.dumps(trains) if trains else "not available"

        prompt = (
            "You are an expert Indian travel agent. Your task is to create a set of distinct travel plans based on a user's request and a catalog of real-time data.\n\n"
            f"**User's Request:** \"{user_query}\"\n"
            f"**Destination:** \"{destination}\"\n\n"
            "**Real-time Data Catalog (You MUST use this data to build the plans):**\n"
            f"- Available Flights: {flights_text}\n"
            f"- Available Hotels: {hotels_text}\n"
            f"- Available Trains: {trains_text}\n\n"
            "**Your Task & Instructions (VERY IMPORTANT):**\n"
            "1. Create 2-3 distinct itinerary options (e.g., budget, luxury, balanced) based on the user's request and the data catalog.\n"
            "2. **CRITICAL:** For EACH itinerary, you MUST select one flight, one hotel, and/or one train *directly* from the data catalogs provided above.\n"
            "3. **DO NOT INVENT or MODIFY data.** The `chosen_flight`, `chosen_hotel`, and `chosen_train` objects in your JSON response **MUST BE an exact, 1-to-1 copy-paste** of one of the JSON objects from the 'Available Flights', 'Available Hotels', or 'Available Trains' data. Do not add, remove, or rename any fields.\n"
            "4. **JSON STRUCTURE IS CRITICAL:** Your response MUST be a single raw JSON object with one key: `plans`. The `plans` key must contain an array of itinerary objects.\n"
            "5. Each itinerary object in the array MUST contain the following keys:\n"
            "   - `plan_name`: A descriptive name (e.g., 'Budget Goa Getaway').\n"
            f"   - `destination`: This MUST be '{destination}'.\n"
            "   - `start_date`, `end_date`: Infer from the query if possible, otherwise use null.\n"
            "   - `total_estimated_cost`: Accurately calculated total cost for the whole trip.\n"
            "   - `chosen_flight`, `chosen_hotel`, `chosen_train`: The **exact JSON object** you copy-pasted from the catalog. Use `null` if not applicable.\n"
            "   - `days`: An array of `DayPlan` objects. **The key MUST be `days`**.\n"
            "6. Each object inside the `days` array must contain:\n"
            "   - `day_number`: The day number (integer).\n"
            "   - `summary`: A brief summary for the day.\n"
            "   - `activities`: An array of `Activity` objects. Each activity object must have a `description` (string) and `time` (string).\n"
            "Adhere strictly to this structure. Do NOT include any extra text, explanations, or markdown formatting outside of the main JSON object."
        )
        return prompt

    def _parse_gemini_result(self, raw_json: dict) -> dict:
        try:
            text_content = raw_json["candidates"][0]["content"]["parts"][0]["text"]
            if text_content.startswith("```json"):
                text_content = text_content[7:-3].strip()
            elif text_content.startswith("```"):
                text_content = text_content[3:-3].strip()

            plans = json.loads(text_content)

            # Restructure chosen_flight, chosen_hotel, chosen_train if needed
            for plan in plans.get("plans", []):
                if isinstance(plan.get("chosen_flight"), dict) and "data" in plan["chosen_flight"]:
                    plan["chosen_flight"] = plan["chosen_flight"]["data"]
                if isinstance(plan.get("chosen_hotel"), dict) and "data" in plan["chosen_hotel"]:
                    plan["chosen_hotel"] = plan["chosen_hotel"]["data"]
                if isinstance(plan.get("chosen_train"), dict) and "data" in plan["chosen_train"]:
                    plan["chosen_train"] = plan["chosen_train"]["data"]

            return plans
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Could not parse Gemini response: {e}")
            logger.error(f"Raw JSON received: {raw_json}")
            return {"error": "Failed to parse AI response.", "details": str(raw_json)}