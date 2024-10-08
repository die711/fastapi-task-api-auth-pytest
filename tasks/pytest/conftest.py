import asyncio
import httpx
import pytest

from api import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def default_client():
    async with httpx.AsyncClient(app=app, base_url='http://app') as client:
        yield client


