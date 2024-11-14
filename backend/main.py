from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from middleware import RateLimiterMiddleware

app = FastAPI()

origins = [
    # "http://localhost:5173",
    # # "http://localhost"
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Ratelimit-Remaining", "X-Ratelimit-Limit", "X-Ratelimit-Retry-After"],
)


app.add_middleware(RateLimiterMiddleware)


@app.get("/api/data")
async def get_data():
    return {"message": "Request Successful!"}

