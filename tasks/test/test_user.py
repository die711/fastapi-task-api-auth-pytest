from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from tasks.database.database import get_database_session
from api import app
from tasks.database.database import Base

SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

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


def test_sign_new_user() -> None:
    payload = {
        'email': 'admintest@admin.com',
        'name': 'andres',
        'surname': 'cruz',
        'website': 'https://desarrollolibre.net',
        'password': '12345'
    }

    response = client.post('/register', json=payload)
    assert response.status_code == 201
    assert response.json() == {
        'message': 'User created successfully'
    }


def test_login_user() -> None:
    payload = {
        'username': 'admintest@admin.com',
        'password': '12345'
    }

    response = client.post('/token', data=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data


def test_logout() -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Token': 'GLRFzgsUXh1ktMOYqeoS0qjs8FqWdQeQ87ODx7yK2jg'
    }

    response = client.delete('/logout', headers=headers)
    assert response.status_code == 200
    assert response.json()['msg'] == 'ok'
