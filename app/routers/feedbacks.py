from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.database import SessionLocal
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Submit feedback (user only)
@router.post("/", response_model=FeedbackOut, description="Users only: Submit feedback.")
def submit_feedback(
    feedback: FeedbackCreate,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=403, detail="Users only can submit feedback.")
    db_feedback = Feedback(
        user_id=user['user_id'],
        feedback_type=feedback.feedback_type,
        parking_lot_id=feedback.parking_lot_id,
        spot_id=feedback.spot_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

#  View all feedback (admin/attendant only)
@router.get("/", response_model=List[FeedbackOut], description="Admin/Attendant: View all feedback.")
def get_all_feedback(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') not in ['admin', 'attendant']:
        raise HTTPException(status_code=403, detail="Admins or attendants only.")
    feedbacks = db.query(Feedback).all()
    return feedbacks

#  View own feedback (user)
@router.get("/my", response_model=List[FeedbackOut], description="Users only: View your feedback.")
def get_my_feedback(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=403, detail="Users only.")
    feedbacks = db.query(Feedback).filter(Feedback.user_id == user['user_id']).all()
    return feedbacks