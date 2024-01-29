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
