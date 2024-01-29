from pydantic import BaseModel


class GenreDTO(BaseModel):
    id: int


class GenreInDTO(BaseModel):
    name: str


class GenreOutDTO(GenreInDTO, GenreDTO):
    class Config:
        from_attributes = True


class GenreOutDetailDTO(GenreOutDTO):
    pass
