from fastapi import FastAPI
from app.api.routers import _routers

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(_routers, prefix="/api")