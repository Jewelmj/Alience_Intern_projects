from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    interaction_id: str
    feedback: str