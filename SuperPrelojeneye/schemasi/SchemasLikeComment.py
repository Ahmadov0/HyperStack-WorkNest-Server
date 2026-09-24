from pydantic import BaseModel, Field, ConfigDict

class Like(BaseModel):
    id: int = Field(
        ..., description="ID of the like"
    )
    user_id: int = Field(..., description="ID of the user")

    author: str = Field(..., description="Author of the like")

    model_config = ConfigDict(
        from_attributes=True
    )

class Comment(BaseModel):
    id: int = Field(..., description="ID of the comment")
    text: str = Field(..., description="Text of the comment")
    author: str = Field(..., description="Author of the comment")

    model_config = ConfigDict(
        from_attributes=True
    )    

class AddComment(BaseModel):
    text: str = Field(..., description="Text of the comment")