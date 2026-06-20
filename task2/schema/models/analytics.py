from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class AnalyticsRecord(BaseModel):
    interaction_id: str
    session_id: str
    query: str
    response_time_ms: int
    retrieved_sources: int
    similarity_scores: List[float]
    created_at: datetime
    feedback: Optional[str] = None