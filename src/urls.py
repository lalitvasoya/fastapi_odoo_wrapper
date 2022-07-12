from fastapi import APIRouter

from odoo_fastapi.src.user_management.urls import router as user_management_router
from odoo_fastapi.src.employee_management.urls import router as employee_management_router


router = APIRouter()

router.include_router(user_management_router, tags=["User Management"], prefix="/user_management")
router.include_router(employee_management_router, tags=["Employee Management"], prefix="/employee_management")
