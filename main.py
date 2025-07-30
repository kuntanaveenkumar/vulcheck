from fastapi import FastAPI
from routers import project_router

app = FastAPI()
app.include_router(project_router.router)
