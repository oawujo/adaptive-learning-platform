
from fastapi import FastAPI, Request
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

CONTENT_ENGINE_URL = "http://content_engine:8003"
LEARNER_DATA_TRACKER_URL = "http://learner_data_tracker:8001"
PERSONALISATION_ENGINE_URL = "http://personalisation_engine:8002"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log")
async def log_learner_action(request: Request):
    json_data = await request.json()
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{LEARNER_DATA_TRACKER_URL}/log", json=json_data)
    return res.json()

@app.post("/recommend")
async def recommend_content(request: Request):
    json_data = await request.json()
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{PERSONALISATION_ENGINE_URL}/recommend", json=json_data)
    return res.json()

@app.post("/generate-content")
async def generate_content(request: Request):
    json_data = await request.json()
    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(f"{CONTENT_ENGINE_URL}/generate", json=json_data)
    try:
        return res.json()
    except Exception:
        print("🔁 Raw response from content engine:", res.text)
        return {"error": "Failed to parse content engine response"}, res.status_code

@app.get("/history")
async def get_history(user_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{LEARNER_DATA_TRACKER_URL}/history?user_id={user_id}")
    return res.json()

@app.get("/")
async def root():
    return {"message": "API Gateway is running"}
