from fastapi import APIRouter
from services import fastf1_service

router = APIRouter()
ff1 = fastf1_service

@router.get("/standings")
def standings():
    return {
        #"events": ff1.get_events(2025),
        "standings": ff1.get_driver_standings(2021),
        #"constructor_std": ff1.get_constructor_standings() 
    }
