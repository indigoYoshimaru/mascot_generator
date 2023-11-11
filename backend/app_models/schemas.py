from pydantic import BaseModel
from typing import Text, Any

class VisitorInfo(BaseModel):
    visitor_id: Text
    status: Text

class Image(BaseModel): 
    path: Text
    # data: Any
    class Config:
        arbitrary_types_allowed = True

class Prompt(BaseModel): 
    prompt: Text

class User(BaseModel):
    visitor_id: Text
    gen_left: int
    class Config:
        orm_mode = True

