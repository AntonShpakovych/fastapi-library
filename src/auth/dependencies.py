from typing import Annotated

from fastapi import Depends

from src.auth.models import User
from src.auth.services.token_service import TokenService
from src.auth.services.user_service import UserService, oauth2_scheme


UserServiceDep = Annotated[UserService, Depends()]
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
