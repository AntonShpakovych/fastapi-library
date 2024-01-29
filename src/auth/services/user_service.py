from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.models import User
from src.auth.schemas.user import UserInDTO
from src.auth.messages import errors
from src.auth.services.token_service import TokenService
from src.auth.repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(self, user: UserInDTO) -> User:
        if await self.get_user_by_email(email=user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.USER_EMAIL_ALREADY_EXISTS
            )

        user.hashed_password = self.hash_password(user.hashed_password)

        return await self.repository.create(user=User(**user.model_dump()))

    async def get_current_user(
            self,
            token: str,
            token_service: TokenService,
    ) -> User:
        token_data = token_service.verify_token(token=token)
        user = await self.get_user_by_email(email=token_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=errors.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    async def authenticate_user(
            self,
            email: str,
            password: str
    ) -> User | HTTPException:
        user = await self.get_user_by_email(email=email)

        if not user or not self.verify_password(
                plain_password=password,
                hashed_password=user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=errors.USER_INCORECT_CREDENTIALS,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_one(identifier=email)

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)
