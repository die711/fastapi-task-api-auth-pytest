from fastapi import APIRouter, Body, status, Depends, Path, Query
from sqlalchemy.orm import Session

from tasks.database.database import get_database_session
from tasks.schemas import TaskWrite, Tag
from tasks.database.task import crud
from tasks.dataexamples import task_with_orm

task_router = APIRouter()


@task_router.get('/paginate', status_code =status.HTTP_200_OK)
def get_paginated(page: int = Query(1, gt=0), size: int = Query(10, gt=0)
                  , db: Session = Depends(get_database_session)):
    return crud.pagination(page, size, db)


@task_router.get('/', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    tasks_db = crud.get_all(db)
    return tasks_db


@task_router.get('/{id}', status_code=status.HTTP_200_OK)
def get_by_id(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    task_db = crud.get_by_id(id, db)
    return task_db


@task_router.post('/', status_code=status.HTTP_201_CREATED)
def add(task: TaskWrite = Body(openapi_examples=task_with_orm), db: Session = Depends(get_database_session)):
    return crud.create(task, db)


@task_router.put('/{id}', status_code=status.HTTP_200_OK)
def update(task: TaskWrite = Body(openapi_examples=task_with_orm), id: int = Path(ge=1),
           db: Session = Depends(get_database_session)):
    return crud.update(id, task, db)


@task_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    crud.delete(id, db)


# *****************tag******************

@task_router.get('/tag/{id_tag}', status_code=status.HTTP_200_OK)
def get_tag_by_id(id_tag: int = Path(ge=1), db: Session = Depends(get_database_session)):
    tag_db = crud.get_tag_by_id(id_tag, db)
    return Tag.model_validate(tag_db)


@task_router.put('/tag/add/{id}', status_code=status.HTTP_200_OK)
def tag_add(id: int = Path(ge=1), id_tag: int = Body(ge=1), db: Session = Depends(get_database_session)):
    return crud.tag_add(id, id_tag, db)


@task_router.delete('/tag/remove/{id}', status_code=status.HTTP_204_NO_CONTENT)
def tag_remove(id: int = Path(ge=1), id_tag: int = Body(ge=1), db: Session = Depends(get_database_session)):
    return crud.tag_remove(id, id_tag, db)
