from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Text
from backend.sql_app import models
from backend.app_models import schemas
from backend.utils import get_logger
from sqlalchemy import select

logger = get_logger(__name__)

# READ


def get_user(db: Session, visitor_id: Text):
    try:
        logger.info(f"{visitor_id=}")
        logger.info(f"{models.User.visitor_id=}")

        user = (
            db.query(models.User).filter(models.User.visitor_id == visitor_id).first()
        )
        if not user:
            model = register_user(db, visitor_id)
            logger.info(f"{model=}")
            # user = (
            #     db.query(models.User)
            #     .filter(models.User.visitor_id == visitor_id)
            #     .first()
            # )

        return model

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e


def get_current_info(db: Session, visitor_id: Text):
    try:
        user = get_user(db, visitor_id)
        generation = get_latest_generation_info(db, visitor_id)

        all_info = schemas.AllInfo(
            user=user,
            generation_info=generation,
        )

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return all_info


def get_user_generation_left(db: Session, visitor_id: Text):
    user = get_user(db, visitor_id)
    return user.gen_left


def get_latest_generation_info(db: Session, visitor_id: Text):
    try:
        user = get_user(db, visitor_id)
        generation = (
            db.query(models.Generation)
            .filter(models.User.visitor_id == visitor_id)
            .order_by(models.Generation.start_time.asc())
        ).first()
        logger.info(f"{generation=}")
        if not generation:
            generation_info = schemas.GenerationInfo(
                prompt=schemas.Prompt(),
                image=schemas.Image(),
            )
            return generation_info

        prompt = get_prompt_by_id(db, generation.prompt_id)
        image = get_image_by_id(db, generation.image_id)
        generation_info = schemas.GenerationInfo(
            prompt=schemas.Prompt(prompt=prompt),
            image=schemas.Image(path=image.path),
            queue_no=generation.queue_no,
            status=generation.status,
            start_time=generation.start_time,
            end_time=generation.end_time,
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return schemas.GenerationInfo(
            prompt=schemas.Prompt(),
            image=schemas.Image(),
        )
    else:
        return generation_info


def get_generation_by_latest_queue(db: Session):
    generation = models.Generation
    return (
        db.query(generation)
        .filter(generation.status == "IN-QUEUE")
        .order_by(generation.queue_no.asc())
        .first()
    )


def get_generation_by_id(db: Session, generation_id: int):
    return (
        db.query(models.Generation)
        .filter(models.Generation.id == generation_id)
        .first()
    )


def get_prompt_by_id(db: Session, prompt_id: int):
    try:
        prompt = db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return schemas.Prompt(prompt="")
    else:
        return prompt


def get_image_by_id(db: Session, image_id: int):
    try:
        image = db.query(models.Image).filter(models.Image.id == image_id).first()

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return schemas.Image(path="")
    else:
        return image


def get_images_by_user(db: Session, visitor_id: Text):
    ...


# CREATE


def __add__(db, model):
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
    except Exception as e:
        raise e
    else:
        return model


def register_user(db: Session, visitor_id: Text):
    db_user = models.User(visitor_id=visitor_id)
    try:
        model = __add__(db, db_user)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


def create_prompt(db: Session, prompt: Text):
    try:
        model = models.Prompt(prompt=prompt)
        model = __add__(model)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


def create_image(db: Session, image_path: Text):
    try:
        model = models.Image(path=image_path)
        model = __add__(model)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


def create_generation(
    db: Session,
    visitor_id: Text,
    prompt: Text,
    start_time: int,
    image_path: Text,
):
    try:
        prompt = create_prompt(db, prompt=prompt)
        image = create_image(db, path=image_path)

        latest_gen = get_generation_by_latest_queue(db)

        generation = models.Generation(
            user_id=visitor_id,
            prompt=prompt.id,
            image=image.id,
            queue_no=latest_gen.queue_no + 1,
            status="IN-QUEUE",
            start_time=start_time,
        )
        model = __add__(generation)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


# UPDATE
