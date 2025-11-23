import uuid
def map_gemini_to_itinerary(gemini_json: dict, user_id: str = None) -> dict:
    trip = {
        "trip_id": str(uuid.uuid4()),
        "user_id": user_id,
        "destination": gemini_json.get("destination"),
        "start_date": gemini_json.get("start_date"),
        "end_date": gemini_json.get("end_date"),
        "total_estimated_cost": gemini_json.get("total_estimated_cost"),
        "days": []
    }
    days = gemini_json.get("days", [])
    for d in days:
        day = {
            "day_number": d.get("day_number"),
            "summary": d.get("summary"),
            "activities": []
        }
        for a in d.get("activities", []):
            day["activities"].append({
                "time": a.get("time"),
                "description": a.get("description"),
                "location": a.get("location"),
                "cost": a.get("cost")
            })
        trip["days"].append(day)
    return trip
