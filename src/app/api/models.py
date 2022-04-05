"""This module holds all the Pydantic models"""
from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    description: str


class NoteDB(NoteSchema):
    id: int
