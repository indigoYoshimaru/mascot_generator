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
        logger.info(f'{visitor_id=}')
        logger.info(f'{models.User.visitor_id=}')

        user = db.query(models.User).filter(models.User.visitor_id == visitor_id).first()
        if not user: 
            msg = register_user(db, visitor_id)
            logger.info(msg)
            user = db.query(models.User).filter(models.User.visitor_id == visitor_id).first()

        return user
    
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e

def get_user_info(db: Session, visitor_id: str): 
    user = get_user(db, visitor_id)
    queue_no = get_user_queue(db, visitor_id)
    

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_queue(db: Session, generation_id: int):
    ...


def get_user_generation_left(db: Session, visitor_id: Text):
    user = get_user(db, visitor_id)
    return user.gen_left


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
        return f"{model} added to database"


def register_user(db: Session, visitor_id: Text):
    
    db_user = models.User(visitor_id=visitor_id)
    try:
        msg = __add__(db, db_user)
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return dict(message=msg)



def create_generation(db: Session, visitor_id: Text, prompt: Text, start_time: int):
    queue_no = get_user_queue(db, visitor_id)
    ...


# UPDATE
