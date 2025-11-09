from fastapi import FastAPI
from app.routers import stories, system
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="StoryShelf API",
    description="A FastAPI-powered microfiction sharing service",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(stories.router)
app.include_router(system.router)