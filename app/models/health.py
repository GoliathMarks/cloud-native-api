from enum import Enum

from pydantic import BaseModel


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"


class HealthResponse(BaseModel):
    status: HealthStatus
    version: str
    service: str
