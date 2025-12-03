from fastapi import FastAPI

from .database import Base, engine
from . import models

# Import routers correctly (relative import)
from .routers_users import router as user_router
from .routers_portfolios import router as portfolio_router
from .routers_signals import router as signals_router

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TradeLens API",
    description="Backend API for the TradeLens investment guidance system",
    version="1.0.0"
)

# Register routers
app.include_router(user_router)
app.include_router(portfolio_router)
app.include_router(signals_router)

@app.get("/")
def root():
    return {"message": "TradeLens API is running"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
