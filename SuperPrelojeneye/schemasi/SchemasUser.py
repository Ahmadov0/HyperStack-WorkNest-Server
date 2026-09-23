from pydantic import BaseModel, Field, ConfigDict

class Auth(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=20, description="Username"
    )
    password: str = Field(
        ..., min_length=6, max_length=20, description="Password"
    )

class User(Auth):
    id: int = Field(..., description="User ID")

    model_config = ConfigDict(
        from_attributes=True
    )


class Login(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=20,
        description="Password"
    )

class UpdateUser(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=20, description="Username"
    )
    password: str = Field(
        ..., min_length=6, max_length=20, description="Password"
    )

class ResponseUser(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., min_length=3, max_length=20, description="Username")

    model_config = ConfigDict(
        from_attributes=True
    )



