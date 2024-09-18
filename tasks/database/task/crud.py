from sqlalchemy.orm import Session, load_only
from fastapi import HTTPException, status

from tasks.database.pagination import PageParams, paginate
from tasks.schemas import TaskWrite, TaskReadComplete
from tasks.database import models


def get_all(db: Session):
    # return db.query(models.Task).options(load_only(models.Task.name, models.Task.description)).all()
    return db.query(models.Task).all()


def pagination(page: int, size: int, db: Session):
    page_params = PageParams(page=page, size=size)
    return paginate(page_params, db.query(models.Task).filter(models.Task.id > 2), TaskReadComplete)


def get_by_id(id: int, db: Session):
    task_db = db.query(models.Task).get(id)
    if task_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return task_db


def create(task: TaskWrite, db: Session):
    task_db = models.Task(
        name=task.name,
        description=task.description,
        status=task.status,
        category_id=task.category_id,
        user_id=task.user_id,
    )

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


def update(id: int, task: TaskWrite, db: Session):
    task_db = get_by_id(id, db)
    task_db.name = task.name
    task_db.description = task.description
    task_db.status = task.status
    task_db.category_id = task.category_id
    db.add(task_db)
    db.commit()
    db.refresh(task_db)

    return task_db


def delete(id: int, db: Session):
    task_db = get_by_id(id, db)
    db.delete(task_db)
    db.commit()


def get_tag_by_id(id_tag: int, db: Session):
    tag = db.query(models.Tag).get(id_tag)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return tag


def tag_add(id: int, id_tag: int, db: Session):
    task = get_by_id(id, db)
    tag = get_tag_by_id(id_tag, db)
    task.tags.append(tag)
    db.add(tag)
    db.commit()
    db.refresh(task)
    return task


def tag_remove(id: int, id_tag: int, db: Session):
    task = get_by_id(id, db)
    tag = get_tag_by_id(id_tag, db)
    task.tags.remove(tag)
    db.add(task)
    db.commit()
    return task
