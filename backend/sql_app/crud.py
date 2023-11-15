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
            user = register_user(db, visitor_id)
            logger.info(f"{user=}")
            # user = (
            #     db.query(models.User)
            #     .filter(models.User.visitor_id == visitor_id)
            #     .first()
            # )

        return user

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e


def get_user_by_id(db: Session, id: Text):
    return db.query(models.User).filter(models.User.id == id).first()


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
            .filter(models.Generation.user_id == user.id)
            .order_by(models.Generation.start_time.desc())
        ).first()
        if not generation:
            generation_info = schemas.GenerationInfo(
                prompt=schemas.Prompt(),
                image=schemas.Image(),
            )
            return generation_info

        logger.info(f"{generation.id=}")
        prompt = get_prompt_by_id(db, generation.prompt_id)
        image = get_image_by_id(db, generation.image_id)
        image_path = image.path.replace('frontend/', '')
        logger.info(f'{image.path=}')
        generation_info = schemas.GenerationInfo(
            prompt=schemas.Prompt(prompt=prompt.prompt),
            image=schemas.Image(path=image_path),
            queue_no=generation.queue_no,
            status=generation.status,
            start_time=generation.start_time,
            end_time=generation.end_time,
        )
        # remember to add update generation left
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
    else:
        return generation_info


def get_generation_by_latest_queue(db: Session):
    generation = models.Generation
    return (
        db.query(generation)
        .filter(generation.status == "IN-QUEUE")
        .order_by(generation.queue_no.desc())
        .first()
    )


def get_generation_in_queue_for_model(db: Session):
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


def get_all_images(db: Session):
    image_obj = db.query(models.Image.path).order_by(models.Image.id.desc()).all()
    return image_obj


def get_running_generation_by_visistor_id(db, visitor_id: Text):
    try:
        user = get_user(db, visitor_id=visitor_id)
        model = models.Generation
        generation = (
            db.query(model)
            .filter(model.user_id == user.id, model.status != "DONE")
            .first()
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return generation


# CREATE


def __add__(db, model):
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
        logger.info(f"{model=}")
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
        model = __add__(db, model)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


def create_image(db: Session, image_path: Text):
    try:
        model = models.Image(path=image_path)
        model = __add__(db, model)
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
        image = create_image(db, image_path=image_path)
        user = get_user(db, visitor_id)
        logger.info(f"{prompt=}")
        logger.info(f"{image=}")

        latest_gen = get_generation_by_latest_queue(db)
        if not latest_gen:
            queue_no = 1
        else:
            queue_no = latest_gen.queue_no + 1
        generation = models.Generation(
            user_id=user.id,
            prompt_id=prompt.id,
            image_id=image.id,
            queue_no=queue_no,
            status="IN-QUEUE",
            start_time=start_time,
            end_time=0,
        )
        model = __add__(db, generation)

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return model


# UPDATE


def update_model_run_all(db: Session, generation: models.Generation):
    try:
        generation = __add__(db, generation)
        user = get_user_by_id(db, generation.user_id)
        user.gen_left -= 1
        user = __add__(db, user)

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return generation
