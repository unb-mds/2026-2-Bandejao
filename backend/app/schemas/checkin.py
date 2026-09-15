from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckInRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campus_id: int
    criado_em: datetime
