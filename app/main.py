from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import router

app = FastAPI(
    title="Task Manager API",
    description="A simple task manager API with JWT auth",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)