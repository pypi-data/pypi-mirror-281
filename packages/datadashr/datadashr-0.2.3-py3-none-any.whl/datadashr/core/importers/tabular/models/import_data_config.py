from pydantic import BaseModel, Extra
from typing import List, Dict
from .source_config import SourceConfig


class ImportDataConfig(BaseModel):
    sources: List[SourceConfig]
    mapping: Dict[str, List[str]] = {}

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.forbid
