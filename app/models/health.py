from pydantic import BaseModel
from enum import Enum


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"


class HealthResponse(BaseModel):
    status: HealthStatus
    version: str
    service: str
