from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class ResourceSet(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel)
    resources: List[T]


class CompleteMetadata(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    image_url: str
    image_url_subdomains: List[str]
    image_height: int
    image_width: int


class BasicMetadata(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    vintage_end: str
