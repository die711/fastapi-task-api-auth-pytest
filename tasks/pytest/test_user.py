import httpx
import pytest


@pytest.mark.asyncio
async def test_hello(default_client: httpx.AsyncClient) -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = await default_client.get('/basic/hello', headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        'message': 'hello world'
    }


@pytest.mark.asyncio
async def test_sing_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        'email': 'admintest@admin.com',
        'name': 'andres',
        'surname': 'cruz',
        'website': 'https://www.desarrollo.net/',
        'password': '11597'
    }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    response = await default_client.post('/register', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {
        'message': 'User created successfully'
    }


@pytest.mark.asyncio
async def test_create_token(default_client: httpx.AsyncClient) -> None:
    payload = {
        'username': 'admintest@admin.com',
        'password': '11597'
    }

    headers = {
        'accept': 'application/json'
    }

    response = await default_client.post('/token', data=payload, headers=headers)

    assert response.status_code == 200
    assert 'access_token' in response.json()


@pytest.mark.asyncio
async def test_logout(default_client: httpx.AsyncClient) -> None:
    headers = {
        'accept': 'application/json',
        'Token': 'gnhotbB5k86RJjCD4DTPXCQYNuofdRSRHoZA0jEpFaY',
        'Content-Type': 'application/json'
    }

    response = await default_client.delete('/logout', headers=headers)
    assert response.status_code == 200
