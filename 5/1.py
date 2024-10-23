from pydantic import BaseModel, EmailStr, Field, PrivateAttr, UUID4, field_validator
from typing import Callable
import uuid


class Book(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int
    available: bool = Field(default=True)
    categories: list[str]

    @field_validator("categories")
    def categories_not_empty_values(cls, v: list[str]):
        if len(v) == 0:
            raise ValueError("categories is required")
        for cat in v:
            if len(cat.strip()) == 0:
                raise ValueError("categories empty values not accepted")
        return v

    def __hash__(self):
        return hash(self.id)


class User(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=1)
    email: EmailStr
    membership_id: str = Field(min_length=1)

    def __hash__(self):
        return hash(self.id)


def log_operation(log: str, err_log: str | None = None):
    def wd(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                print("LOG:", log)
            except BaseException as e:
                if err_log is not None:
                    print("ERROR:", err_log)
                raise e

        return wrapper

    return wd


class BookNotAvailable(BaseException):
    pass


class Library(BaseModel):
    books: list[Book]
    users: list[User]

    __books_to_users: dict[Book, User] = PrivateAttr(default={})

    def find_book(
        self,
        *,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
    ) -> Book | None:
        if title is None and author is None and year is None:
            return None
        for book in self.books:
            if (
                (title is None or (title is not None and title == book.title))
                and (author is None or (author is not None and author == book.author))
                and (year is None or (year is not None and year == book.year))
            ):
                return book
        return None

    @log_operation("took book", "error on taking book")
    def add_book(self, book: Book, user: User) -> None:
        try:
            book_index = self.books.index(book)
        except ValueError:
            raise BookNotAvailable

        if user not in self.users:
            raise BookNotAvailable

        if not self.books[book_index].available:
            raise BookNotAvailable

        self.books[book_index].available = False
        self.__books_to_users[self.books[book_index]] = user

    def is_book_borrow(self, book: Book) -> bool:
        try:
            book_index = self.books.index(book)
        except ValueError:
            raise BookNotAvailable

        return self.books[book_index].available

    @log_operation("return book", "error on returning book")
    def return_book(self, book: Book) -> None:
        try:
            book_index = self.books.index(book)
        except ValueError:
            raise ValueError

        if self.books[book_index] not in self.__books_to_users:
            raise ValueError

        self.books[book_index].available = True
        del self.__books_to_users[self.books[book_index]]

    def total_books(self) -> int:
        return len(self.books)


book1 = Book(
    title="Clean code", author="Robert Martin", year=2008, categories=["coding"]
)
book2 = Book(
    title="Clean architecture", author="Robert Martin", year=2017, categories=["coding"]
)

vasya = User(name="Vasya", email="vasya@test.ru", membership_id="1")
petya = User(name="Petya", email="petya@test.ru", membership_id="2")

library = Library(books=[book1, book2], users=[vasya, petya])

book = library.find_book(title="Clean code")

if book:
    library.add_book(book=book, user=vasya)
    library.is_book_borrow(book=book)
    library.return_book(book=book)
    library.add_book(book=book, user=petya)
    # проверим лог на вывод ошибки
    library.add_book(book=book, user=vasya)
