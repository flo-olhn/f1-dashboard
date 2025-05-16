from fastapi import APIRouter
from services import fastf1_service
from datetime import datetime

router = APIRouter()
ff1 = fastf1_service


@router.get("/standings")
async def standings():
    return {
        "standings": ff1.get_standings(datetime.now().year),
    }

@router.get("/standings/{season}")
async def standings(season: int = None):
    if season is None:
        season = datetime.now().year
    return {
        "standings": ff1.get_standings(season),
    }

@router.get("/events")
async def events():
    return {
        "events": ff1.get_events(datetime.now().year)
    }

@router.get("/events/{season}")
async def events(season: int = None):
    if season is None:
        season = datetime.now().year
    return {
        "events": ff1.get_events(season)
    }
