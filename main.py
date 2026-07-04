from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users,posts,votes, oath
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
app.include_router(posts.router)
app.include_router(votes.router)
app.include_router(oath.router)



@app.get("/")
def root():
    return {"message": "idk and idc lol"}