from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.models import Base


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True, index=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="genre"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)

    books: Mapped[list["Book"]] = relationship(
        back_populates="authors",
        secondary="books_authors"
    )

    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "last_name",
            name="uq_authors_first_name_last_name"
        ),
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(index=True, unique=True)
    file_path: Mapped[str]
    date_published: Mapped[datetime] = mapped_column(
        server_default=text(
            "TIMEZONE('utc', now())"
        )
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            "genres.id",
            ondelete="CASCADE"
        )
    )

    genre: Mapped["Genre"] = relationship(
        back_populates="books"
    )
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books",
        secondary="books_authors"
    )


class BookAuthor(Base):
    __tablename__ = "books_authors"

    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "authors.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey(
            "books.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
