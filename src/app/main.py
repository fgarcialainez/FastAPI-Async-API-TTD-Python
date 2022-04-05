"""This module holds the entry point of the app"""
from fastapi import FastAPI

from app.api import ping
from app.db import database, engine, metadata

# Create all tables stored in this metadata
metadata.create_all(engine)

# Create the FastAPI instance
app = FastAPI()


# Startup handler
@app.on_event("startup")
async def startup():
    await database.connect()


# Shutdown handler
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Include the available routers
app.include_router(ping.router)
