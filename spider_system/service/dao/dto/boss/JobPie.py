from typing import Optional
from pydantic import BaseModel

class JobPie(BaseModel):
    job_name: str
    city_name: Optional[str] = None
