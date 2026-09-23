from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from SuperPrelojeneye.DataBase.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    posts: Mapped[list["PostModel"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    body: Mapped[str]
    private: Mapped[bool]

    Author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["UserModel"] = relationship(back_populates="posts")

