# backend/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class PlayerRequest(BaseModel):
    name: str

class PlayerResponse(BaseModel):
    id: int | None = None
    name: str
    runs: int
    wickets: int
    model_config = ConfigDict(from_attributes=True)

class NLAskRequest(BaseModel):
    query: str

class NLAskResponse(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    visualization_hint: Optional[str]
    sql: Optional[str]
    