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


@router.post("/txt2img/generate", dependencies=[Depends(cookie)])
def generate_image(
    generation_data: schemas.GenerationRequest,
    session_data: SessionData = Depends(verifier),
    db: Session = Depends(get_db),
):
    """Generate image:
    Args:
        generation_data:
            - prompt: string
            - option_id: int
    Return:
        response: GenerationInfo
    """
    from backend.app_models.txt2img import merge_prompt
    from datetime import datetime
    import os

    try:
        visitor_id = session_data.visitor_id

        # 0. check if a generation is running or no generation left
        gen_left = crud.get_user_generation_left(db, visitor_id=visitor_id)
        response_model = crud.get_running_generation_by_visistor_id(
            db,
            visitor_id = visitor_id,
        )
        logger.info(f'{gen_left=}')
        logger.info(f'{response_model=}')
        if not gen_left or response_model:
            raise MemoryError(
                "You either have exceeded your generation or having a running generation"
            )

        # 1. merge prompt
        prompt = merge_prompt(generation_data)
        logger.info(f"{prompt=}")
        # 2. create start time
        curr_dt = datetime.now()
        start_time = int(round(curr_dt.timestamp()))
        # 3. create image path as placeholder
        image_path = os.path.join(
            "frontend/images",
            visitor_id,
        )
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        image_path = os.path.join(image_path, f'{start_time}.png')
        # 4. write db
        response_model = crud.create_generation(
            db,
            visitor_id=visitor_id,
            prompt=prompt,
            start_time=start_time,
            image_path=image_path,
        )
        logger.info(
            f"Create new generation {response_model} from {visitor_id} at {curr_dt}"
        )
    except MemoryError as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return response_model


@router.get("/txt2img/get-example-prompt")
def get_example_prompt():
    from backend.app_models.txt2img import get_example_prompt

    try:
        prompt = get_example_prompt()
        logger.info(prompt)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return prompt
