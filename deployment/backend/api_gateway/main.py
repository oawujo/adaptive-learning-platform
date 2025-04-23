#
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# import os
#
# app = FastAPI()
#
# CONTENT_ENGINE_URL = "https://content-engine-6gzt.onrender.com"
# LEARNER_DATA_TRACKER_URL = "https://learner-data-tracker-6gzt.onrender.com"
# PERSONALISATION_ENGINE_URL = "https://personalisation-engine-6gzt.onrender.com"
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://adaptive-learning-ui-6gzt.onrender.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# @app.post("/log")
# async def log_learner_action(request: Request):
#     json_data = await request.json()
#     async with httpx.AsyncClient() as client:
#         res = await client.post(f"{LEARNER_DATA_TRACKER_URL}/log", json=json_data)
#     return res.json()
#
# @app.post("/recommend")
# async def recommend_content(request: Request):
#     json_data = await request.json()
#     async with httpx.AsyncClient() as client:
#         res = await client.post(f"{PERSONALISATION_ENGINE_URL}/recommend", json=json_data)
#     return res.json()
#
# @app.post("/generate-content")
# async def generate_content(request: Request):
#     json_data = await request.json()
#     async with httpx.AsyncClient(timeout=60.0) as client:
#         res = await client.post(f"{CONTENT_ENGINE_URL}/generate", json=json_data)
#     try:
#         return res.json()
#     except Exception:
#         print("🔁 Raw response from content engine:", res.text)
#         return {"error": "Failed to parse content engine response"}, res.status_code
#
# @app.get("/history")
# async def get_history(user_id: str):
#     async with httpx.AsyncClient() as client:
#         res = await client.get(f"{LEARNER_DATA_TRACKER_URL}/history?user_id={user_id}")
#     return res.json()
#
# @app.get("/")
# async def root():
#     return {"message": "API Gateway is running"}
#
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Load external service URLs from environment variables (for deployment flexibility)
CONTENT_ENGINE_URL = os.getenv("CONTENT_ENGINE_URL", "https://content-engine-6gzt.onrender.com")
LEARNER_DATA_TRACKER_URL = os.getenv("LEARNER_DATA_TRACKER_URL", "https://learner-data-tracker-6gzt.onrender.com")
PERSONALISATION_ENGINE_URL = os.getenv("PERSONALISATION_ENGINE_URL", "https://personalisation-engine-6gzt.onrender.com")

# CORS: Allow only the deployed frontend (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://adaptive-learning-ui-6gzt.onrender.com/log"],
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
    except Exception as e:
        print("🔁 Content engine returned non-JSON:", await res.aread())
        return {"error": "Failed to parse content engine response"}, res.status_code

@app.get("/history")
async def get_history(user_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{LEARNER_DATA_TRACKER_URL}/history?user_id={user_id}")
    return res.json()

@app.get("/")
async def root():
    return {"message": "API Gateway is live and responding"}