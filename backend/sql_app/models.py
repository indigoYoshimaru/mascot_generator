from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base # coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Image(Base):
    __tablename__ = 'images'

    id = Column(Numeric, primary_key=True, unique=True)
    path = Column(Text, nullable=False)


class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Numeric, primary_key=True, unique=True)
    prompt = Column(Text, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Numeric, primary_key=True, nullable=False, unique=True)
    visitor_id = Column(Text, primary_key=True, nullable=False)
    gen_left = Column(Numeric, nullable=False, server_default=text("10"))


class Generation(Base):
    __tablename__ = 'generation'

    id = Column(Numeric, primary_key=True, unique=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    prompt_id = Column(ForeignKey('prompts.id'), nullable=False)
    image_id = Column(ForeignKey('images.id'))
    queue_no = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)
    start_time = Column(Integer)
    end_time = Column(Integer)

    image = relationship('Image')
    prompt = relationship('Prompt')
    user = relationship('User')
