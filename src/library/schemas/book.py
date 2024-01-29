from datetime import date

from pydantic import BaseModel


class BookDTO(BaseModel):
    id: int


class BookInDTO(BaseModel):
    title: str
    date_published: date


class BookInCreateDTO(BookInDTO):
    genres: list[int]
    authors: list[int]


class BookInUpdateDTO(BookInDTO):
    pass


class BookUploadFileDTO(BookInUpdateDTO):
    filename: str | None = None

    class Config:
        from_attributes = True


class BookOutDTO(BookDTO):
    title: str

    class Config:
        from_attributes = True


class BookOutDetailDTO(BookOutDTO):
    date_published: date
    filename: str | None = None

    class Config:
        from_attributes = True
