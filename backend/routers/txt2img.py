from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.utils import get_logger
from backend.app_models.schemas import VisitorInfo
from backend.sql_app import crud
from backend.app_models import schemas
from backend.sql_app.database import get_db
from backend.app_models.session import cookie, SessionData, verifier


router = APIRouter()
logger = get_logger(name=__name__)


@router.post("/generate", dependencies=[Depends(cookie)])
async def generate_image(
    generation_data: None, 
    session_data: SessionData = Depends(verifier)):
    ...
    """Generate image: 
    Args: 
        generation_data: class includes: 
            - prompt
            - option_id
    Return:
        response: class include:
            - visitor_id
            - queue
            - generation left
            - image_path
    """