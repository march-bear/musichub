from fastapi import FastAPI

from app.routes import tracks

app = FastAPI()
app.include_router(tracks.router)
