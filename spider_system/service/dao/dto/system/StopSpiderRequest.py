
from pydantic import BaseModel


class StopSpiderRequest(BaseModel):
    spider_id: str
