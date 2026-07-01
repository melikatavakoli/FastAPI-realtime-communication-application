from fastapi import Query
from pydantic import BaseModel


class PaginationParam(BaseModel):
    skip: int
    limit: int
    
    @property
    def offset(self):
        return(self.page-1)*self.page_size
    
def pagination_param(skip: int=Query(0, ge=0), limit:int=Query(10, ge=1, le=100),)->PaginationParam:
    return PaginationParam(skip=skip, limit=limit,)


# T = TypeVar("T")
# class PaginatedResponse(GenericModel, Generic[T]):
#     total: int
#     page: int
#     page_size: int
#     items: list[T]