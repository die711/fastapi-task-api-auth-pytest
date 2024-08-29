import httpx
import pytest
from sqlalchemy.orm import Session

from tasks.database.database import get_database_session
from tasks.database.task import crud
from tasks.database import models


@pytest.mark.asyncio
async def test_create_task(default_client: httpx.AsyncClient) -> None:
    payload = {
        'name': 'Task 2',
        'description': 'Description Task',
        'status': 'done',
        'user_id': 1,
        'category_id': 1
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = await default_client.post('/tasks/', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()['name'] == payload['name']


@pytest.mark.asyncio
async def test_update_task(default_client: httpx.AsyncClient) -> None:
    payload = {
        'id': 2,
        'name': 'Task put',
        'description': 'Description Task put',
        'status': 'pending',
        'user_id': 1,
        'category_id': 1
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = await default_client.put(f'/tasks/{payload['id']}', json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()['name'] == payload['name']


@pytest.mark.asyncio
async def test_all_tasks(default_client: httpx.AsyncClient,
                         db: Session = next(get_database_session())) -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    tasks = crud.get_all(db)
    response = await default_client.get('/tasks/', headers=headers)
    assert response.status_code == 200
    assert len(tasks) == len(response.json())


@pytest.mark.asyncio
async def test_by_id_task(default_client: httpx.AsyncClient, db: Session = next(get_database_session())) -> None:
    id = 2
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    task = crud.get_by_id(id, db)
    response = await default_client.get(f'/tasks/{id}', headers=headers)
    assert response.status_code == 200
    assert id == response.json()['id']
    assert task.name == response.json()['name']


@pytest.mark.asyncio
async def test_delete_task(default_client: httpx.AsyncClient, db: Session = next(get_database_session())) -> None:
    id = 2
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = await default_client.delete(f'/tasks/{id}', headers=headers)
    task = db.query(models.Task).get(id)
    assert response.status_code == 204
    assert task is None


@pytest.mark.asyncio
async def test_delete_task_not_found(default_client: httpx.AsyncClient,
                                     db: Session = next(get_database_session())) -> None:
    id = 2
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = await default_client.delete(f'/tasks/{id}', headers=headers)
    task = db.query(models.Task).get(id)
    assert response.status_code == 404
    assert task is None
