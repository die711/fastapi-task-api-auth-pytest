from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

basic_router = APIRouter()
phone_pattern = r'(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})'


def pagination(page: Optional[int] = 1, limit: Optional[int] = 10):
    return {
        'page': page - 1,
        'limit': limit
    }


@basic_router.get('/pagination')
def index(page: dict = Depends(pagination)):
    return page



@basic_router.get('/phone')
def phone_route(phone: str = Query(pattern=phone_pattern, example='686-2028-370')):
    return {
        'phone': phone
    }


@basic_router.get('/page2')
def page1(page: int = Query(1, gt=0, title='Pagina a visualizar'),
          size: int = Query(10, le=100)):
    return {
        'page': page,
        'size': size
    }


@basic_router.get('/page/{page}')
def page2(page: int = Path(gt=10),
          size: int = Query(gt=10, le=100)):
    return {
        'page': page,
        'size': size
    }


@basic_router.get('/hello')
def hello_world() -> dict:
    return {
        'message': 'hello world'
    }
