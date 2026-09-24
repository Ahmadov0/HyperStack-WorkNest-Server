from pydantic import BaseModel, Field, ConfigDict
from SuperPrelojeneye.schemasi.SchemasUser import ResponseUser
from typing import Optional

class AddPost(BaseModel):
    title: str = Field(min_length=3, max_length=20, description="Title of the post")
    content: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Content of the post"
    )
    body: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Body of the post"
    )
    private: bool = Field(default=False, description="Whether or not the post is private")

    Author_id: int = Field(..., description="ID of the user creating the post")

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    body: str
    private: bool
    author: Optional[ResponseUser] = None
    likes_count: Optional[int] = 0
    likes_users: Optional[list[int]] = []

    model_config = ConfigDict(from_attributes=True)

class UpdatePost(BaseModel):
    title: str = Field(min_length=3, max_length=20, description="Title of the post")
    content: str = Field(min_length=3, max_length=20, description="Content of the post")
    body: str = Field(min_length=3, max_length=1000, description="Body of the post")
    private: bool = Field(default=False, description="Whether or not the post is private")


