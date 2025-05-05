# ParkLogic

A simple parking management system built with FastAPI, SQLAlchemy, and SQLite.

## Features

- User registration and authentication (JWT)
- Role-based access: user, admin, attendant
- Manage parking lots, floors, and spots (CRUD)
- Book and cancel parking spots (users)
- Block/unblock spots for maintenance (admin/attendant)
- Submit and view feedback
- User profile management and password change
- Clean, modular code structure

## Project Structure
- app/
- models/         # SQLAlchemy models
- routers/        # FastAPI routers (endpoints)
- schemas/        # Pydantic schemas
- database.py     # DB connection and session
- main.py         # FastAPI app entrypoint


## Getting Started

1. **Clone the repo**
    ```bash
    git clone <your-repo-url>
    cd ParkLogic
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    Create a `.env` file in the `app/` directory with:
    ```
    JWT_SECRET_KEY=your_secret_key_here
    ```

4. **Run the app**
    ```bash
    uvicorn app.main:app --reload
    ```

5. **Open the API docs**

    Visit [http://localhost:8000/docs](http://localhost:8000/docs) or  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

## Roles & Access

- **User:** Book/cancel spots, view/update profile, submit feedback
- **Admin:** Manage lots/floors/spots, view all bookings/feedback, block spots for maintenance
- **Attendant:** Block/unblock spots for maintenance, view bookings/feedback

## Notes

- Uses SQLite for easy local development.
- All endpoints require authentication (register/login to get a JWT token).
- Role checks are enforced in each endpoint.

---

**Happy Parking! 🚗**

