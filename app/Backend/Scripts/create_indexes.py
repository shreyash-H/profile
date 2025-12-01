#!/usr/bin/env python3
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "portfolio")

async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    print("Creating index: status_checks.timestamp (desc)")
    await db.status_checks.create_index([("timestamp", -1)], name="idx_status_timestamp")
    print("Index creation complete")

if __name__ == "__main__":
    asyncio.run(main())
