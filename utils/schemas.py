from pydantic import BaseModel

class OwnedStatusSchema(BaseModel):
    id: str
    owned: bool