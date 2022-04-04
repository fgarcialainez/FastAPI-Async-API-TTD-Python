"""This module holds the entry point of the app"""
from fastapi import FastAPI

# Create the FastAPI instance
app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
