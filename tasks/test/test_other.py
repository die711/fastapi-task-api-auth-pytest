from tasks import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api import app
from tasks.authentication import authentication
from tasks.database.database import get_database_session

client = TestClient(app)


@pytest.fixture(scope='module')
async def access_token(db: Session = next(get_database_session())) -> str:
    user = authentication.authenticate('user@example.com', '11597', db)
    return authentication.create_access_token(user, db).access_token


def test_protected_router(access_token: str) -> None:
    headers = {
        'Content-Type': 'application/json',
        'token': access_token
    }

    response = client.get('/auth/get-tasks2', headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert 'hello' in data


def test_protected_route(access_token: str) -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = client.get('/auth/get-tasks4', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'hello' in data
