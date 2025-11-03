# backend/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class PlayerRequest(BaseModel):
    name: str

class PlayerResponse(BaseModel):
    id: int | None = None
    name: str
    runs: int

    model_config = ConfigDict(from_attributes=True)

class NLAskRequest(BaseModel):
    query: str

class NLAskResponse(BaseModel):
    sql: str
    results: List[Dict[str, Any]]