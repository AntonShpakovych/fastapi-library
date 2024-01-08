from pydantic import BaseModel, EmailStr, Field


class UserDTO(BaseModel):
    email: EmailStr
    is_superuser: bool


class UserInDTO(UserDTO):
    hashed_password: str = Field(alias="password")


class UserOutDTO(UserDTO):
    id: int

    class Config:
        from_attributes = True


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
