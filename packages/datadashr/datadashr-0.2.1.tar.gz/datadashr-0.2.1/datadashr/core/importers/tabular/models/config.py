from pydantic import BaseModel, Extra


class SQLConfig(BaseModel):
    dialect: str
    driver: str
    host: str
    port: int
    database: str
    username: str
    password: str

    class Config:
        extra = Extra.forbid
