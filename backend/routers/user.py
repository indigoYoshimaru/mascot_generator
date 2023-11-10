from fastapi import APIRouter, Depends
from backend.utils import get_logger
from backend.app_models.user import VisitorInfo

router = APIRouter()
logger = get_logger(name="user")


@router.post("/user/register")
async def register_user(visitor_info: VisitorInfo):
    try: 
        visitor_id = visitor_info.visitor_id
        logger.info(f"{visitor_id=}")
        response_data = {"message": "User registration successful"}
        return response_data
    except Exception as e: 
        logger.error(f"{str(e)}")
        raise e



@router.get("/user/get-current")
def get_current_user(visitor_info: VisitorInfo):
    visitor_id = visitor_info.visitor_id
    logger.info(f"{visitor_id=}")
    return dict(visitor_id=visitor_id)
