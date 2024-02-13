from pydantic import BaseModel, EmailStr


class TokenDTO(BaseModel):
    token_type: str


class TokenRefreshDTO(BaseModel):
    refresh_token: str


class TokenAccessDTO(TokenDTO):
    access_token: str


class TokenAccessRefreshDTO(TokenAccessDTO, TokenRefreshDTO):
    pass


class TokenDataDTO(BaseModel):
    email: EmailStr | None = None
