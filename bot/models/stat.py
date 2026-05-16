from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserUpdate(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    user_id: int
    chat_id: int
    is_command: bool = False

class Anomaly(BaseModel):
    id: Optional[int] = None
    user_id: int
    chat_id: int
    detected_at: datetime
    type: str = "unknown"