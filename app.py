from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from models import get_db, Category, Experience, Booking, Review

# ------------------- FASTAPI SETUP -------------------
app = FastAPI()

# allow frontend requests from any origin (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Talii API"}

# ------------------- CATEGORY ROUTES -------------------
class CategorySchema(BaseModel):
    name: str

@app.post("/categories")
def create_category(category: CategorySchema, session: Session = Depends(get_db)):
    existing = session.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(name=category.name)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@app.get("/categories")
def get_categories(session: Session = Depends(get_db)):
    return session.query(Category).all()

@app.get("/categories/{category_id}")
def get_category(category_id: int, session: Session = Depends(get_db)):
    category = session.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.patch("/categories/{category_id}")
def update_category(category_id: int, category: CategorySchema, session: Session = Depends(get_db)):
    existing = session.query(Category).get(category_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    existing.name = category.name
    session.commit()
    session.refresh(existing)
    return existing

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_db)):
    existing = session.query(Category).get(category_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(existing)
    session.commit()
    return {"message": "Category deleted successfully"}

# ------------------- EXPERIENCE ROUTES -------------------
class ExperienceSchema(BaseModel):
    title: str
    description: str
    price: float
    location: Optional[str] = None
    image_url: Optional[str] = None
    category_id: int

@app.post("/experiences")
def create_experience(experience: ExperienceSchema, session: Session = Depends(get_db)):
    new_exp = Experience(**experience.dict())
    session.add(new_exp)
    session.commit()
    session.refresh(new_exp)
    return new_exp

@app.get("/experiences")
def get_experiences(session: Session = Depends(get_db)):
    return session.query(Experience).all()

@app.get("/experiences/{experience_id}")
def get_experience(experience_id: int, session: Session = Depends(get_db)):
    exp = session.query(Experience).get(experience_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return exp

@app.patch("/experiences/{experience_id}")
def update_experience(experience_id: int, experience: ExperienceSchema, session: Session = Depends(get_db)):
    exp = session.query(Experience).get(experience_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    for key, value in experience.dict().items():
        setattr(exp, key, value)
    session.commit()
    session.refresh(exp)
    return exp

@app.delete("/experiences/{experience_id}")
def delete_experience(experience_id: int, session: Session = Depends(get_db)):
    exp = session.query(Experience).get(experience_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    session.delete(exp)
    session.commit()
    return {"message": "Experience deleted successfully"}

# ------------------- BOOKING ROUTES -------------------
class BookingSchema(BaseModel):
    username: str
    experience_id: int
    date: str  # ISO date string
    people: int

@app.post("/bookings")
def create_booking(booking: BookingSchema, session: Session = Depends(get_db)):
    new_booking = Booking(
        username=booking.username,
        experience_id=booking.experience_id,
        date=booking.date,
        people=booking.people
    )
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    return new_booking

@app.get("/bookings/user/{username}")
def get_user_bookings(username: str, session: Session = Depends(get_db)):
    return session.query(Booking).filter(Booking.username == username).all()

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, session: Session = Depends(get_db)):
    booking = session.query(Booking).get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(booking)
    session.commit()
    return {"message": "Booking deleted successfully"}

# ------------------- REVIEW ROUTES -------------------
class ReviewSchema(BaseModel):
    username: str
    experience_id: int
    rating: int
    comment: str

@app.post("/reviews")
def create_review(review: ReviewSchema, session: Session = Depends(get_db)):
    new_review = Review(**review.dict())
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review

@app.get("/reviews/experience/{experience_id}")
def get_reviews_for_experience(experience_id: int, session: Session = Depends(get_db)):
    return session.query(Review).filter(Review.experience_id == experience_id).all()
