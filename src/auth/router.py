from starlette import status

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import (
    UserServiceDep,
    TokenServiceDep
)
from src.auth.schemas.user import (
    UserInDTO,
    UserOutDTO,
)
from src.auth.schemas.token import (
    TokenRefreshDTO,
    TokenAccessRefreshDTO,
    TokenAccessDTO
)
from src.auth.messages import description


router = APIRouter()


@router.post(
    "/register",
    response_model=UserOutDTO,
    status_code=status.HTTP_201_CREATED
)
async def register(user: UserInDTO, user_service: UserServiceDep):
    return await user_service.register_user(user=user)


@router.post(
    "/token",
    response_model=TokenAccessRefreshDTO,
    description=description.CREATE_ACCESS_TOKEN
)
async def login_for_access_token_and_refresh(
        user_service: UserServiceDep,
        token_service: TokenServiceDep,
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    data = {"sub": user.email}

    access_token = token_service.create_access_token(data=data)
    refresh_token = token_service.create_refresh_token(data=data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


@router.get(
    "/refresh",
    response_model=TokenAccessDTO
)
async def refresh_access_token(
        token: TokenRefreshDTO,
        token_service: TokenServiceDep,
        user_service: UserServiceDep
):

    access_token = await token_service.refresh_access_token(
        token=token.refresh_token,
        user_by_email_callable=user_service.get_user_by_email
    )

    return {"access_token": access_token, "token_type": "Bearer"}
