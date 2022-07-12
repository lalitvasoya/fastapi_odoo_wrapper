from fastapi import APIRouter

router = APIRouter()


@router.get('/user')
def get_user():
    return {"first_name": "lalit", "last_name": "vasoya"}
