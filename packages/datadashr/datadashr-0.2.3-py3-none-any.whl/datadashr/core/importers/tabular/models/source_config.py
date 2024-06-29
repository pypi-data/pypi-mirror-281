import pandas as pd
import polars as pl
from pydantic import BaseModel, field_validator, Extra
from typing import Union, Dict, Any
from .config import SQLConfig


class SourceConfig(BaseModel):
    source_name: str
    source_type: str
    description: str = "No description provided"
    delete_table: bool = False
    connection_string: Union['SQLConfig', None] = None
    data: Union[pd.DataFrame, pl.DataFrame, None] = None
    file_path: Union[str, None] = None
    host: Union[str, None] = None
    username: Union[str, None] = None
    password: Union[str, None] = None
    index: Union[str, None] = None
    query: Union[str, None] = None
    filter: Dict[str, Any] = {}
    save_to_vector: bool = False

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.forbid

    @field_validator('source_type')
    def check_source_type(cls, value):
        if value not in ['pandas', 'polars', 'csv', 'sql', 'elasticsearch', 'parquet']:
            raise ValueError(f"Unsupported source type: {value}")
        return value
