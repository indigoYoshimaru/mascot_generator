from pydantic import BaseModel
from typing import Text, Any


class VisitorInfo(BaseModel):
    visitor_id: Text


class Image(BaseModel):
    path: Text = ""

    # data: Any
    class Config:
        arbitrary_types_allowed = True


class Prompt(BaseModel):
    prompt: Text = ""


class User(BaseModel):
    visitor_id: Text
    gen_left: int

    class Config:
        orm_mode = True


class GenerationInfo(BaseModel):
    prompt: Prompt
    image: Image
    queue_no: int = 0
    start_time: int = 0
    end_time: int = 0
    status: Text = ""

class GenerationRequest(BaseModel): 
    prompt: Text = ''
    option: int = 1
    
class AllInfo(BaseModel):
    user: User
    generation_info: GenerationInfo
