from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def only_get():
    return {"message":"got you"}









"""my_post = [{"title":"title 1", "content":"content 1", "id":1}, {"title":"title 2", "content":"content 2", "id":2},{"title":"title 3", "content":"content 3", "id":3}]
def find_post(id):
    for p in my_post:
        if p['id'] == id :
            return p
        
def find_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i"""
            