from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)

    events = relationship("Event", back_populates="season")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, ForeignKey("seasons.id"))
    round = Column(Integer)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    session1 = Column(String)  # e.g., "Practice 1", "Qualifying", "
    session1_date = Column(DateTime)
    session2 = Column(String)  
    session2_date = Column(DateTime)
    session3 = Column(String)  
    session3_date = Column(DateTime)
    session4 = Column(String)  
    session4_date = Column(DateTime)
    session5 = Column(String) 
    session5_date = Column(DateTime)
    status = Column(String)  # "passed" or "upcoming"
    created_at = Column(DateTime)

    season = relationship("Season", back_populates="events")
