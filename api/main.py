from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import router

app = FastAPI()
app.include_router(router.router)
app.mount("/public", StaticFiles(directory="public"), name="public")
