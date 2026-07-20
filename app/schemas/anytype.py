from pydantic import BaseModel
from typing import Optional

class AnyTypeSpace(BaseModel):
    id: str
    name: str
    description: Optional[str] = None    
    object: Optional[str] = None
