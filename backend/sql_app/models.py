# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, unique=True)
    path = Column(String, nullable=False)


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, unique=True)
    prompt = Column(String, nullable=False)


t_sqlite_sequence = Table(
    "sqlite_sequence", metadata, Column("name", NullType), Column("seq", NullType)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    visitor_id = Column(String, nullable=False)
    gen_left = Column(Integer, nullable=False, server_default=text("10"))


class Generation(Base):
    __tablename__ = "generation"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    prompt_id = Column(ForeignKey("prompts.id"), nullable=False)
    image_id = Column(ForeignKey("images.id"))
    queue_no = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    start_time = Column(Integer)
    end_time = Column(Integer)

    image = relationship("Image")
    prompt = relationship("Prompt")
    user = relationship("User")
