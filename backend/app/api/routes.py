from fastapi import APIRouter
from services import fastf1_service
from datetime import datetime
from database.database import SessionLocal
from database.models import Season, Event


router = APIRouter()
ff1 = fastf1_service

db = SessionLocal()
current_season = datetime.now().year


@router.get("/standings")
async def standings():
    return {
        "standings": ff1.get_standings(),
    }

@router.get("/standings/{season}")
async def standings(season: int):
    return {
        "standings": ff1.get_standings(season),
    }

@router.get("/events")
async def events():
    data = db.query(Event).filter_by(year=current_season).all()
    return {"events": data}
    

@router.get("/events/{season}")
async def events(season: int):
    data = db.query(Event).filter_by(year=season).all()
    return {"events": data}
