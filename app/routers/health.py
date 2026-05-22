from fastapi import APIRouter

from app.models.health import HealthResponse, HealthStatus

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse, summary="Health check")
async def health_check():
    """Returns the current health status of the service."""
    return HealthResponse(
        status=HealthStatus.healthy,
        version="0.1.0",
        service="cloud-native-api",
    )
