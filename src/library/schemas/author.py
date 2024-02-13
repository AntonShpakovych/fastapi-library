from pydantic import BaseModel, computed_field


class AuthorDTO(BaseModel):
    id: int


class AuthorInDTO(BaseModel):
    first_name: str
    last_name: str


class AuthorOutDTO(AuthorInDTO, AuthorDTO):
    pass


class AuthorOutDetailDTO(AuthorInDTO, AuthorDTO):
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
