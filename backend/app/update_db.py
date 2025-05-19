# update_db.py

from database.database import Base, SessionLocal
from database.models import Season, Event
from services.fastf1_service import get_events  # your existing FastF1 logic
import datetime


def update():
  for s in [2021, 2022, 2023, 2024, 2025]:
    # 1. Get FastF1 event data
    event_data = get_events(s)
    season_year = event_data["season"]
    passed = event_data["passed_events"]
    upcoming = event_data["upcoming_events"]

    # 2. Connect to DB
    db = SessionLocal()

    # 3. Create tables if not already created
    Base.metadata.create_all(bind=db.get_bind())

    # 4. Check if season already exists
    season = db.query(Season).filter_by(id=season_year).first()
    if not season:
        season = Season(id=season_year, created_at=datetime.datetime.now())
        db.add(season)
        db.commit()
        db.refresh(season)

    # 5. Add events
    def add_events(events, status: str):
        for e in events:
            existing = db.query(Event).filter_by(year=season.id, round=e['RoundNumber']).first()
            if existing:
                # update event status if event is passed
                if status == "upcoming" and e['Session5DateUtc'] < datetime.datetime.now():
                    existing.status = "passed"
                    db.commit()

            event = Event(
                year=season.id,
                round=e['RoundNumber'],
                name=e['EventName'],
                location=e['Location'],
                country=e['Country'],
                session1 = e['Session1'],
                session1_date= e['Session1DateUtc'],
                session2 = e['Session2'],
                session2_date= e['Session2DateUtc'],
                session3 = e['Session3'],
                session3_date= e['Session3DateUtc'],
                session4 = e['Session4'],
                session4_date= e['Session4DateUtc'],
                session5 = e['Session5'],
                session5_date= e['Session5DateUtc'],
                status=status,
                created_at=datetime.datetime.now()
            )
            db.add(event)

    add_events(passed, "passed")
    add_events(upcoming, "upcoming")

    # 6. Commit all changes
    db.commit()
    db.close()

    print(f"✅ Season {season_year} data stored successfully.")

if __name__ == "__main__":
    update()
