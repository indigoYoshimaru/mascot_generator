from pydantic import BaseModel
from typing import Text

class VisitorInfo(BaseModel):
    visitor_id: Text
    status: Text
