from fastapi import Depends, HTTPException, status, APIRouter, Header, Query
from fastapi.security import APIKeyHeader
from typing import Annotated
from sqlalchemy.orm import Session

from tasks.database.database import get_database_session
from tasks.database.models import User, AccessToken
from tasks.authentication.authentication import verify_access_token, verify_access_token_auth_schema

auth_router = APIRouter()
api_key_header = APIKeyHeader(name="Token")
API_KEY_TOKEN = 'SECRET 123'


def protected_route(db: Session = Depends(get_database_session), token: str = Depends(api_key_header)):
    access_token = db.query(AccessToken).filter(AccessToken.access_token == token).first()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def validate_token(token: Annotated[str | None, Header()] = None) -> None:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def authenticate(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != API_KEY_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return token


@auth_router.get('/get-tasks', dependencies=[Depends(validate_token)])
def protected_router() -> dict:
    return {
        'hello': 'Fast Api'
    }


@auth_router.get('/get-tasks2', dependencies=[Depends(protected_route)])
def protected_route2() -> dict:
    return {
        'hello': 'Fast API'
    }


@auth_router.get('/get-tasks3')
def protected_router3(user: User = Depends(verify_access_token)) -> dict:
    return {
        'hello': user.name
    }


@auth_router.get('/get-tasks4')
def protected_router4(user: User = Depends(verify_access_token_auth_schema)) -> dict:
    return {
        'hello': user.name
    }


@auth_router.get('/get-tasks5')
def protected_router5(token: str = Depends(api_key_header)) -> dict:
    if token != API_KEY_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {
        'hello': 'Fast Api'
    }


@auth_router.get('/get-tasks6')
def protected_router6(page: int = Query(1, ge=1, le=20),
                      size: int = Query(5, ge=5, le=20),
                      token: str = Depends(authenticate)) -> dict:
    return {
        'page': page,
        'size': size,
        'token': token
    }
