# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------- DATABASE SETUP ----------------------
engine = create_engine("sqlite:///talii.db", echo=True)
Session = sessionmaker(bind=engine)

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()

# ---------------------- TABLES ----------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)

class Experience(Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    location = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.now)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)
    experience_id = Column(Integer, ForeignKey("experiences.id"))
    date = Column(DateTime, nullable=False)
    people = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)
    experience_id = Column(Integer, ForeignKey("experiences.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
