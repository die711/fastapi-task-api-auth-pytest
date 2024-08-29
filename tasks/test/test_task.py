from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from api import app
from tasks.database import models
from tasks.database.database import Base
from tasks.database.database import get_database_session
from tasks.database.task import crud

SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_database_session] = override_get_db
client = TestClient(app)


def test_create_task() -> None:
    payload = {
        'name': 'Tasks 1 Fast Api',
        'description': 'Description Task',
        'status': 'pending',
        'user_id': 1,
        'category_id': 1
    }

    response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json()['name'] == payload['name']


def test_update_task() -> None:
    payload = {
        'id': 1,
        'name': 'Task 1 Fast api update',
        'description': 'Description Task update',
        'status': 'done',
        'user_id': 1,
        'category_id': 2
    }

    response = client.put(f'/tasks/{payload['id']}', json=payload)
    assert response.status_code == 200
    assert response.json()['name'] == payload['name']


def test_all_tasks(db: Session = next(override_get_db())) -> None:
    tasks = crud.get_all(db)
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(tasks) == len(response.json())


def test_by_id(db: Session = next(override_get_db())) -> None:
    id = 1
    task = crud.get_by_id(id, db)
    response = client.get('/tasks/1')
    assert response.status_code == 200
    assert id == response.json()['id']
    assert task.name == response.json()['name']


def test_delete_task(db: Session = next(override_get_db())) -> None:
    id = 2
    response = client.delete(f'/tasks/{id}')
    task = db.query(models.Task).get(id)
    assert response.status_code == 204
    assert task is None


def test_delete_task_not_exists(db: Session = next(override_get_db())) -> None:
    id = 1
    response = client.delete(f'/tasks/{id}')
    task = db.query(models.Task).get(id)
    assert response.status_code == 404
    assert task is None
