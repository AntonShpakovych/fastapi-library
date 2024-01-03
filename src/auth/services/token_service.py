from datetime import datetime, timedelta
from typing import Callable

from jose import jwt
from starlette import status

from fastapi import HTTPException

from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY
)

from src.auth.messages import errors
from src.auth.schemas import TokenDataDTO


class TokenService:
    def create_access_token(self, data: dict) -> str:
        return self._create_token(
            data=data,
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expire_time=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(
            data=data,
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expire_time=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    def verify_token(self, token: str) -> TokenDataDTO | HTTPException:
        try:
            return self._decode_token(token=token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=errors.JWT_TOKEN_EXPIRED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=errors.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_access_token(
            self,
            token: str,
            user_by_email_callable: Callable
    ) -> str:
        token_data = self.verify_token(token=token)
        user = await user_by_email_callable(email=token_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=errors.JWT_TOKEN_INVALID,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self.create_access_token(data={"sub": user.email})

    def _create_token(
            self,
            data: dict,
            algorithm: str,
            secret_key: str,
            expire_time: int
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=expire_time
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

        return encoded_jwt

    def _decode_token(self, token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return TokenDataDTO(email=email)
