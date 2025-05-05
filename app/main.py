from fastapi import FastAPI
from app.routers import (
    auth,
    parkinglot,
    floor,
    spot,
    booking,
    user,
    feedbacks
)
from app.models import users, parkinglot as parkinglot_model, parkingRecords, feedback
from app.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ParkLogic API",
    description="A simple parking management system built with FastAPI.",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(parkinglot.router)
app.include_router(floor.router)
app.include_router(spot.router)
app.include_router(booking.router)
app.include_router(user.router)
app.include_router(feedbacks.router)  # Uncomment when ready

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to ParkLogic API!"}