from fastapi import APIRouter, Depends

from src.auth.schemas import UserInDTO, UserOutDTO
from src.auth.service import UserService


router = APIRouter()


@router.post("/register", response_model=UserOutDTO, status_code=201)
async def register(user: UserInDTO, user_service: UserService = Depends()):
    return await user_service.create_user(user=user)
