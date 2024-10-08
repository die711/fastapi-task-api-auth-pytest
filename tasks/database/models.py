from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy import Table
from sqlalchemy.types import String, Integer, Text, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from tasks.database.database import Base
from tasks.schemas import StatusType


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    description = Column(Text())
    status = Column(Enum(StatusType))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship('Category', lazy='joined', back_populates='tasks')
    user = relationship('User', lazy='joined', back_populates='tasks')
    tags = relationship('Tag', lazy='joined', secondary='task_tag', back_populates='tasks')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    tasks = relationship('Task', back_populates='category')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    surname = Column(String(20))
    email = Column(String(50))
    website = Column(String(50))
    hashed_password = Column(String(255))

    tasks = relationship('Task', back_populates='user', lazy='joined')


class AccessToken(Base):
    __tablename__ = 'access_tokens'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    access_token = Column(String(255))
    expiration_date = Column(DateTime(timezone=True))

    user = relationship('User', lazy='joined')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    tasks = relationship('Task', secondary='task_tag', back_populates='tags')


task_tag = Table(
    'task_tag',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
