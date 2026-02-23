from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users
import modles
from database import engine


modles.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "idk and idc lol"}