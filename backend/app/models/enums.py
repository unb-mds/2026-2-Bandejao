import enum


class TipoRefeicao(str, enum.Enum):
    CAFE_DA_MANHA = "cafe_da_manha"
    ALMOCO = "almoco"
    JANTAR = "jantar"


class Categoria(str, enum.Enum):
    BEBIDA = "bebida"
    PANIFICACAO = "panificacao"
    OPCAO_EXTRA = "opcao_extra"
    GORDURA = "gordura"
    SALADA_1 = "salada_1"
    SALADA_2 = "salada_2"
    MOLHO_SALADA = "molho_salada"
    PRATO_PRINCIPAL = "prato_principal"
    GUARNICAO = "guarnicao"
    SOPA = "sopa"
    TORRADA = "torrada"
    ACOMPANHAMENTO = "acompanhamento"
    SOBREMESA = "sobremesa"
    FRUTA = "fruta"


class TipoDieta(str, enum.Enum):
    COMUM = "comum"
    PADRAO = "padrao"
    OVOLACTOVEGETARIANO = "ovolactovegetariano"
    VEGETARIANO_ESTRITO = "vegetariano_estrito"
