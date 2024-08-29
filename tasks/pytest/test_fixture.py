import pytest
from tasks.schemas import Category


@pytest.fixture
def category() -> Category:
    return Category(id=1, name='Book FastAPI')


def test_category_name(category: Category) -> None:
    assert category.name == 'Book FastAPI'


def test_category_name_not(category: Category) -> None:
    assert category.name != 'Book FastAPI 2'
