from pydantic import BaseModel, Field
from typing import Text, Any


class VisitorInfo(BaseModel):
    visitor_id: Text


class Image(BaseModel):
    path: Text = Field(default="")

    # data: Any
    class Config:
        arbitrary_types_allowed = True


class Prompt(BaseModel):
    prompt: Text = Field(default="")


class User(BaseModel):
    visitor_id: Text
    gen_left: int

    class Config:
        orm_mode = True


class GenerationInfo(BaseModel):
    prompt: Prompt
    image: Image
    queue_no: int = Field(default=0)
    start_time: int = Field(default=0)
    end_time: int = Field(default=0)
    status: Text = Field(default="")


class GenerationRequest(BaseModel):
    prompt: Text = Field(default="")
    option: int = Field(default=1)


class AllInfo(BaseModel):
    user: User
    generation_info: GenerationInfo
