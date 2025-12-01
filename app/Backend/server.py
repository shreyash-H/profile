#!/usr/bin/env python3
"""Production-ready FastAPI backend (server.py)

Features:
- Index creation on startup
- Paginated /api/status endpoint
- Contact form persistence
- CORS using env var
- Health endpoint
"""
import os
import logging
from datetime import datetime
from typing import List

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("portfolio_backend")

app = FastAPI(title="Portfolio Backend")

# Environment
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "portfolio")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")  # comma-separated or '*'

# Setup DB
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DB_NAME]

# CORS config
origins = [o.strip() for o in CORS_ORIGINS.split(",")] if CORS_ORIGINS != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Health(BaseModel):
    status: str = Field("ok")
    time: datetime = Field(default_factory=datetime.utcnow)

class ContactIn(BaseModel):
    name: str
    email: str
    message: str

@app.on_event("startup")
async def startup_create_indexes():
    """Create recommended indexes if they don't exist."""
    try:
        await db.status_checks.create_index([("timestamp", -1)], name="idx_status_timestamp")
        await db.contacts.create_index([("created_at", -1)], name="idx_contacts_created_at")
        logger.info("Ensured indexes exist.")
    except Exception as e:
        logger.warning("Index creation warning: %s", e)

@app.get("/api/health", response_model=Health)
async def health():
    return Health()

@app.get("/api/status")
async def get_status(limit: int = Query(50, ge=1, le=500), skip: int = Query(0, ge=0)):
    """Paginated status checks. Default limit 50, max 500."""
    try:
        cursor = db.status_checks.find({}, projection={"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        return {"items": results, "count": len(results), "limit": limit, "skip": skip}
    except Exception as e:
        logger.exception("DB query failed: %s", e)
        raise HTTPException(status_code=500, detail="Database query failed")

@app.post("/api/contact")
async def submit_contact(payload: ContactIn):
    try:
        doc = {
            "name": payload.name,
            "email": payload.email,
            "message": payload.message,
            "created_at": datetime.utcnow()
        }
        await db.contacts.insert_one(doc)
        return {"status": "ok"}
    except Exception as e:
        logger.exception("Failed to save contact: %s", e)
        raise HTTPException(status_code=500, detail="Failed to save message")

# Simple root to confirm server running
@app.get("/")
async def root():
    return {"message": "Portfolio backend running."}
