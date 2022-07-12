# urls for user_management
from fastapi import APIRouter

from odoo_fastapi.src.employee_management.views.employee_management import router as employee_router

router = APIRouter()

router.include_router(employee_router)

