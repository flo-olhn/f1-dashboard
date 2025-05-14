from fastapi import FastAPI
from api import routes

app = FastAPI(title="F1 Data API")

app.include_router(routes.router)

print("Starting FastAPI application...")
