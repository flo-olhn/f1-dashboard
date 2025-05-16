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
