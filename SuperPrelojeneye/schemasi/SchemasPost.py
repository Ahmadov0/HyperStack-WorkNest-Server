from pydantic import BaseModel, Field, ConfigDict
from SuperPrelojeneye.schemasi.SchemasUser import ResponseUser

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

class Post(AddPost):
    id: int = Field(..., description="ID of the post")
    author: ResponseUser = Field(..., description="Author of the post")

    model_config = ConfigDict(
        from_attributes=True
    )

class UpdatePost(BaseModel):
    title: str = Field(min_length=3, max_length=20, description="Title of the post")
    content: str = Field(min_length=3, max_length=20, description="Content of the post")
    body: str = Field(min_length=3, max_length=1000, description="Body of the post")
    private: bool = Field(default=False, description="Whether or not the post is private")


