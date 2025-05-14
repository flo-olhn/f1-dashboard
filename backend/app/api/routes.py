from fastapi import APIRouter
from services.fastf1_service import get_driver_standings

router = APIRouter()

@router.get("/standings")
def standings():
    return get_driver_standings()
