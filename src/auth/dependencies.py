from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from src.auth.models import User
from src.auth.repositories.user_repository import UserRepository
from src.auth.services.token_service import TokenService
from src.auth.services.user_service import UserService, oauth2_scheme
from src.auth.messages import errors
from src.dependencies import AsyncSession


def get_user_repository(db: AsyncSession):
    return UserRepository(db=db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep):
    return UserService(repository=repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
TokenServiceDep = Annotated[TokenService, Depends()]


async def current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
    token_service: TokenServiceDep
) -> User:
    return await user_service.get_current_user(
        token=token,
        token_service=token_service
    )


async def admin_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
    token_service: TokenServiceDep
) -> User:
    user = await user_service.get_current_user(
        token=token,
        token_service=token_service
    )

    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=errors.ADMIN_CURRENT_USER
        )
    return user


CurrentUserDep = Annotated[User, Depends(current_user)]
AdminCurrentUserDep = Annotated[User, Depends(admin_current_user)]
