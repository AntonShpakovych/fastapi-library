from datetime import date
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
        back_populates="genres",
        secondary="books_genres"
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
    filename: Mapped[str] = mapped_column(nullable=True)
    read_only: Mapped[bool] = mapped_column(server_default="f")
    date_published: Mapped[date]
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="books",
        secondary="books_genres"
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


class BookGenre(Base):
    __tablename__ = "books_genres"

    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            "genres.id",
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
