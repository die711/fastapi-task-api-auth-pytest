from typing import Generic, List, TypeVar
from pydantic import BaseModel, conint
from sqlalchemy.orm import Query


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10


T = TypeVar("T")


class PagedResponseSchema(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]


def paginate(page_params: PageParams, query: Query, response_schema: BaseModel) -> PagedResponseSchema[T]:
    paginated_query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size).all()

    return PagedResponseSchema(
        total=query.count(),
        page=page_params.page,
        size=page_params.size,
        results=[response_schema.model_validate(item) for item in paginated_query]
    )
