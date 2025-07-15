from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.api.routes import calorie, auth, meal
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limiter import limiter


app = FastAPI()
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please slow down and try again later."}
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routes
app.include_router(calorie.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(meal.router, prefix="/api")
