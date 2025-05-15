from fastapi import APIRouter
from services import fastf1_service

router = APIRouter()
ff1 = fastf1_service

@router.get("/standings")
def standings():
    return {
        "standings": ff1.get_standings(),
    }

@router.get("/events")
def events():
    return {
        "events": ff1.get_events()
    }
