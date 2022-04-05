"""This module holds some API endpoints implementation"""
from fastapi import APIRouter

# Instantiate an API router
router = APIRouter()


@router.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}
