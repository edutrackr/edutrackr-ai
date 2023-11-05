from fastapi import APIRouter
from api.auth import APIKeyValidation
from api.routes.analytics import router as analytics_router


router = APIRouter(prefix="/api", dependencies=[APIKeyValidation])
router.include_router(analytics_router)
