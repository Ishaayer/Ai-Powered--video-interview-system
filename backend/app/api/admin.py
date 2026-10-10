from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role

from app.schemas.user import AdminDashboardResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def dashboard(
    user=Depends(require_role("admin")),
):
   return AdminDashboardResponse(
    message="Welcome Admin",
    user=user.email,
)