from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status


from src.auth.repository import UserRepository
from src.auth.schemas import UserInDTO
from src.auth.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository = repository

    async def create_user(self, user: UserInDTO) -> User:
        if await self.__is_user_exists_by_email(email=user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )
        hashed_password = pwd_context.hash(user.hashed_password)
        user.hashed_password = hashed_password

        return await self.repository.create(User(**user.model_dump()))

    async def __is_user_exists_by_email(self, email: str) -> User:
        return await self.repository.get(identifier=email)
