from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CategoriaReclamacao


class ReclamacaoCreate(BaseModel):
    # O limite vale depois de remover os espaços das pontas (CA-RF08-01).
    model_config = ConfigDict(str_strip_whitespace=True)

    categoria: CategoriaReclamacao
    descricao: str = Field(min_length=1, max_length=1000)


class ReclamacaoConfirmacao(BaseModel):
    """Confirmação ao autor. Não promete encaminhamento ao RU nem publicação (CA-RF08-03)."""

    id: int
    mensagem: str = "Reclamação registrada."


class ReclamacaoEquipeRead(BaseModel):
    """Leitura interna da equipe. Não expõe a identidade de quem registrou."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cardapio_id: int
    categoria: CategoriaReclamacao
    descricao: str
    criado_em: datetime
