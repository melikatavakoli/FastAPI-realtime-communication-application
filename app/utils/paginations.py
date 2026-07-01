from fastapi import Query
from pydantic import BaseModel


class PaginationParam(BaseModel):
    skip: int
    limit: int
    
def pagination_param(skip: int=Query(0, ge=0), limit:int=Query(10, ge=1, le=100),)->PaginationParam:
    return PaginationParam(skip=skip, limit=limit,)