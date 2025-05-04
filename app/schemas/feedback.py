from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    user_id: int
    feedback_type: str  # 'service', 'lot', 'spot'
    parking_lot_id: int = None
    spot_id: int = None
    rating: int
    comment: str

class FeedbackOut(BaseModel):
    id: int
    user_id: int
    feedback_type: str
    parking_lot_id: int = None
    spot_id: int = None
    rating: int
    comment: str
    created_at: str  # You can use str for simplicity, or datetime if you want

    class Config:
        orm_mode = True