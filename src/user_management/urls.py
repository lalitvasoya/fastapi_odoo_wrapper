# urls for user_management
from fastapi import APIRouter

from odoo_fastapi.src.user_management.views.user_management import router as user_router
from odoo_fastapi.src.user_management.views.authentications import router as authentication_router


router = APIRouter()

router.include_router(user_router)
router.include_router(authentication_router)
