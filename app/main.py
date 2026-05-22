from fastapi import FastAPI
from app.routers import health, items

app = FastAPI(
    title="Cloud Native API",
    description="A cloud-native REST API built with FastAPI",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(items.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Cloud Native API is running", "docs": "/docs"}
