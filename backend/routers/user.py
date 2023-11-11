from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.utils import get_logger
from backend.app_models.schemas import VisitorInfo
from backend.sql_app import crud
from backend.app_models import schemas
from backend.utils import get_db

router = APIRouter()
logger = get_logger(name=__name__)


@router.post("/user/register")
def register_user(
    visitor_info: VisitorInfo,
    db: Session = Depends(get_db),
):
    try:
        visitor_id = visitor_info.visitor_id
        logger.info(f"{visitor_id=}")

        response_data = crud.register_user(db=db, visitor_id=visitor_id)
        return response_data
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e


@router.get("/user/{visitor_id}", response_model=schemas.User)
def get_current_user(
    visitor_id: str,
    db: Session = Depends(get_db),
):
    
    try: 
        logger.info(f"{visitor_id=}")
        logger.info(f'{db=}')
        user = crud.get_user(db, visitor_id=visitor_id)
        assert user, 'No user found'
        logger.info(f"{user=}")
        return user
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
