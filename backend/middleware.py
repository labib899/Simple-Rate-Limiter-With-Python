from fastapi.responses import JSONResponse
import redis
import time
from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))  
REFILL_TIME = int(os.getenv("REFILL_TIME", 60))  

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

with open("redis_lua.lua", "r") as lua_file:
    LUA_SCRIPT = lua_file.read()

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        global_key = 'global_key'
        current_time = int(time.time())

        remaining_tokens = redis_client.eval(
            LUA_SCRIPT,
            1,
            global_key,
            RATE_LIMIT,
            REFILL_TIME,
            current_time
        )

        if remaining_tokens < 0:
            reset_time = redis_client.ttl(global_key)
            if reset_time < 0:  
                reset_time = REFILL_TIME

            headers = {
                "X-Ratelimit-Remaining": "0",
                "X-Ratelimit-Limit": str(RATE_LIMIT),
                "X-Ratelimit-Retry-After": str(reset_time),

                "Access-Control-Allow-Origin": "*",  
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "X-Ratelimit-Remaining, X-Ratelimit-Limit, X-Ratelimit-Retry-After",
            }
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429, headers=headers)

        
        response = await call_next(request)
        response.headers["X-Ratelimit-Remaining"] = str(remaining_tokens)
        response.headers["X-Ratelimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-Ratelimit-Retry-After"] = str(REFILL_TIME)
        
        return response
