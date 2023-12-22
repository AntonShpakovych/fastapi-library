from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    email: EmailStr


class UserInDTO(UserDTO):
    hashed_password: str


class UserOutDTO(UserDTO):
    id: int

    class Config:
        from_attributes = True
