        # MCP Smart Trip - MCP Server (Gemini Integration)

        This is a sample prototype server that demonstrates how to connect an MCP server to a Gemini-like API for travel itinerary generation.


        ## Contents
        - app/: Python app with FastAPI
        - assets/: example mockup PNGs
        - requirements.txt
        - .env.sample


        ## Setup (step-by-step)

1. Unzip the project (instructions below).
2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.sample` and fill your GEMINI_API_KEY and URL.

5. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

6. Example curl test:
```bash
curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"user_id":"u1","query":"Plan a 3-day trip to Goa for 2 adults, budget 20000"}'
```

## Notes
- Replace GEMINI endpoint & payload formatting to match your provider. See code comments in `app/gemini_client.py`.
- For production, secure CORS and use a proper secrets manager.
