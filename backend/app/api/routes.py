from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import fastf1_service
from datetime import datetime
from database import update_db
from database.database import SessionLocal
from database.models import Event

router = APIRouter()
ff1 = fastf1_service


@router.get("/standings")
async def standings():
    update_db.update()
    return {
        "standings": ff1.get_standings(datetime.now().year),
    }

@router.get("/standings/{season}")
async def standings(season: int):
    return {
        "standings": ff1.get_standings(season),
    }

@router.get("/events")
async def events():
    return {
        "events": ff1.get_events(datetime.now().year)
    }

@router.get("/events/{season}")
async def events(season: int):
    return {
        "events": ff1.get_events(season)
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dev/events")
def read_events(db: Session = Depends(get_db)):
    return db.query(Event).all()
