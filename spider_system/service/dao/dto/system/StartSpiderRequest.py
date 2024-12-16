from pydantic import BaseModel
class StartSpiderRequest(BaseModel):
    spider_name: str
    spider_args: dict
    description: str

