from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class SpreadsheetCreate(BaseModel):
    name: str

class SpreadsheetResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class RecordCreate(BaseModel):
    data: Dict  # e.g., {"name": "John", "age": 30}

class RecordResponse(BaseModel):
    id: int
    data: Dict
    created_at: datetime

    class Config:
        from_attributes = True

class RecordUpdate(BaseModel):
    data: Dict

class SearchQuery(BaseModel):
    query: str  # e.g., "name:John" or "age>30"
