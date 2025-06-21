from pydantic import BaseModel
from typing import Any, Generic, List, TypeVar, Union

T = TypeVar("T", bound=Union[BaseModel, List[BaseModel], Any])


class AppResponse(BaseModel, Generic[T]):
    success: bool = True
    data: dict | list[dict]
