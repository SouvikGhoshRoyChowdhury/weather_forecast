from fastapi import FastAPI

from src.routes import weather_api

# Creating FastAPI object and include our weather api router
app = FastAPI()

app.include_router(weather_api.router)

