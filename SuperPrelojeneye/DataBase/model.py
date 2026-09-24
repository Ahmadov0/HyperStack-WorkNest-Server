from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Text
from SuperPrelojeneye.DataBase.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    posts: Mapped[list["PostModel"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[list["LikeModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    body: Mapped[str]
    private: Mapped[bool]

    Author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["UserModel"] = relationship(back_populates="posts")
    likes: Mapped[list["LikeModel"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class LikeModel(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["UserModel"] = relationship(back_populates="likes")
    post: Mapped["PostModel"] = relationship(back_populates="likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),
    )

class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["UserModel"] = relationship(back_populates="comments")
    post: Mapped["PostModel"] = relationship(back_populates="comments")