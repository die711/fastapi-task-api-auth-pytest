from fastapi import APIRouter, Depends, Query, Path, Header, File
from typing import Annotated
from tasks.schemas import UserRead

annotated_router = APIRouter()


def get_current_user():
    return UserRead(
        id=1,
        name='diego',
        surname='resendiz',
        email='di_564@hotmail.com',
        website='https://google.com'
    )


phone_pattern = r'(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})'
CurrentUser = Annotated[UserRead, Depends(get_current_user)]


@annotated_router.get('/items')
def read_items(user: UserRead = Depends(get_current_user)):
    return {
        'user': user
    }


@annotated_router.post('/items')
def create_item(user: UserRead = Depends(get_current_user)):
    return {
        'user': user
    }


@annotated_router.delete('/items')
def delete_item(user: UserRead = Depends(get_current_user)):
    return {
        'user': user
    }


@annotated_router.get('/items1')
def read_items(user: CurrentUser):
    return {
        'user': user
    }


@annotated_router.post('/items1')
def create_items(user: CurrentUser):
    return {
        'user': user
    }


@annotated_router.delete('/items1')
def delete_item(user: CurrentUser):
    return {
        'user': user
    }


@annotated_router.get('/page')
def page_route(page: Annotated[int, Query(ge=1, le=20, description='Esta es la pagina que quieres ver')] = 1,
               size: Annotated[int, Query(ge=5, le=20, title='Cuantos registros por pagina')] = 5):
    return {
        'page': page,
        'size': size
    }


@annotated_router.get('/phone/{phone}')
def phone_router(phone: Annotated[str, Path(pattern=phone_pattern)]):
    return {
        'phone': phone
    }


@annotated_router.get('/token')
def validate_token(token: Annotated[str, Header]):
    print(token)
    return {
        'token': token
    }


@annotated_router.post('/files')
def create_file(file: Annotated[bytes, File()]):
    return {
        'file_size': len(file)
    }
