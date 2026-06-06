from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
import math

T = TypeVar("T")


class PaginationParams:
    def __init__(self, page: int = 1, size: int = 20):
        self.page = max(1, page)
        self.limit = min(size, 100)
        self.skip = (self.page - 1) * self.limit


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int = 0

    def model_post_init(self, __context):
        if self.size > 0:
            self.pages = math.ceil(self.total / self.size)
