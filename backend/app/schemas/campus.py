from pydantic import BaseModel, ConfigDict


class CampusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str