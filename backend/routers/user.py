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


@router.post("/user/get-user", response_model=schemas.User)
async def get_current_user(
    visitor_id: VisitorInfo,
    response: Response,
    db: Session = Depends(get_db),
):
    from backend.app_models.session import create_session

    try:
        logger.info(f"{visitor_id=}")
        visitor_id = visitor_id.visitor_id
        logger.info(f"{db=}")
        user = crud.get_user(db, visitor_id=visitor_id)
        assert user, "No user found"
        logger.info(f"{user=}")

        await create_session(
            visitor_id=visitor_id,
            response=response,
        )
        return user
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.get(
    "/get-current-info",
    response_model=schemas.AllInfo,
    dependencies=[Depends(cookie)],
)
def get_current_info(
    session_data: SessionData = Depends(verifier),
    db: Session = Depends(get_db),
):
    try:
        logger.info(f"{session_data=}")
        visitor_id = session_data.visitor_id
        assert visitor_id, "Invalid visitor id"
        current_info = crud.get_current_info(db, visitor_id)

    except AssertionError as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(
            status_code=404, detail=dict(message=f"{visitor_id} not found")
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return current_info


# @router.post("/user/get-queue-no/")
# def get_queue_no(
#     visitor_id: str,
#     generation_id: str,
#     db: Session = Depends(get_db),
# ):
#     try:
#         # logger.info(f"{visitor_info=}")
#         # visitor_id = visitor_info.visitor_id
#         logger.info(f"{visitor_id} getting queue number")
#         queue_no = crud.get_user_queue(db, generation_id)
#     except Exception as e:
#         logger.error(f"{type(e).__name__}: {e}")
#         raise e
#     else:
#         logger.info(f"{visitor_id=}: {queue_no=}")
#         return queue_no


# @router.post("/user/get-generation-left/{visitor_id}")
# def get_generation_left(
#     visitor_id: str,
#     db: Session = Depends(get_db),
# ):
#     try:
#         logger.info(f"{visitor_id} getting generation left")
#         user = crud.get_user(db, visitor_id)
#         assert user, "Invalid user"
#         generation_left = crud.get_user_generation_left(db, visitor_id)

#     except AssertionError as e:
#         logger.error(f"{type(e).__name__}: {e}")
#         raise HTTPException(
#             status_code=404,
#             detail=dict(message=f"{visitor_id} not found"),
#         )
#     except Exception as e:
#         logger.error(f"{type(e).__name__}: {e}")
#         raise e
#     else:
#         logger.info(f"{visitor_id=}: {generation_left=}")
#         return generation_left


@router.get("/user/get-image-history/{visitor_id}")
def get_image_history(
    visitor_id: str,
    db: Session = Depends(get_db),
):
    ...
