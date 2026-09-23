from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models import Campus, Cardapio, ItemCardapio
from app.models.enums import TipoDieta, TipoRefeicao
from app.schemas.cardapio import (
    ALERGENOS_VALIDOS,
    CardapioImportacao,
    CardapioRead,
    ImportacaoResultado,
)

router = APIRouter(prefix="/cardapios", tags=["cardapio"])

@router.get("/", response_model=list[CardapioRead])
def listar_cardapios(
    campus_id: int | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    tipo_refeicao: TipoRefeicao | None = Query(default=None),
    tipo_dieta: TipoDieta | None = Query(
        default=None, description="Restringe os itens retornados a esta dieta"
    ),
    excluir_alergenos: list[str] | None = Query(
        default=None,
        description=f"Alérgenos a excluir dos itens. Opções: {', '.join(sorted(ALERGENOS_VALIDOS))}",
    ),
    db: Session = Depends(get_db),
) -> list[CardapioRead]:
    for alergeno in excluir_alergenos or []:
        if alergeno not in ALERGENOS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Alérgeno inválido: {alergeno}. Opções: {', '.join(sorted(ALERGENOS_VALIDOS))}",
            )

    query = db.query(Cardapio).options(selectinload(Cardapio.itens))
    if campus_id is not None:
        query = query.filter(Cardapio.campus_id == campus_id)
    if data_inicio is not None:
        query = query.filter(Cardapio.data >= data_inicio)
    if data_fim is not None:
        query = query.filter(Cardapio.data <= data_fim)
    if tipo_refeicao is not None:
        query = query.filter(Cardapio.tipo_refeicao == tipo_refeicao)

    cardapios = query.order_by(Cardapio.data).all()
    resultado = [CardapioRead.model_validate(c) for c in cardapios]

    if tipo_dieta is not None or excluir_alergenos:
        for cardapio in resultado:
            itens = cardapio.itens
            if tipo_dieta is not None:
                itens = [i for i in itens if i.tipo_dieta == tipo_dieta]
            for alergeno in excluir_alergenos or []:
                itens = [i for i in itens if not getattr(i, f"contem_{alergeno}")]
            cardapio.itens = itens

    return resultado


@router.post("/importacao", response_model=ImportacaoResultado, tags=["importacao"])
def importar_cardapio(
    importacao: CardapioImportacao, db: Session = Depends(get_db)
) -> ImportacaoResultado:
    """Insere a saída da extração e permite reprocessar a mesma semana sem duplicar dados."""
    campus = db.query(Campus).filter(Campus.nome == importacao.campus).first()
    if campus is None:
        campus = Campus(nome=importacao.campus)
        db.add(campus)
        # Obtém o id do campus antes de criar cardápios que dependem dele na mesma transação.
        db.flush()

    itens_processados = 0
    for refeicao in importacao.refeicoes:
        cardapio = (
            db.query(Cardapio)
            .filter(
                Cardapio.campus_id == campus.id,
                Cardapio.data == refeicao.data,
                Cardapio.tipo_refeicao == refeicao.tipo_refeicao,
            )
            .first()
        )
        if cardapio is None:
            cardapio = Cardapio(
                campus_id=campus.id,
                data=refeicao.data,
                tipo_refeicao=refeicao.tipo_refeicao,
                fonte_pdf_url=importacao.fonte_pdf_url,
            )
            db.add(cardapio)
            db.flush()
        else:
            cardapio.fonte_pdf_url = importacao.fonte_pdf_url
            # A fonte é semanal: uma nova extração substitui a versão anterior da refeição.
            for item in cardapio.itens:
                db.delete(item)
            db.flush()

        for item in refeicao.itens:
            # Converte a lista da extração nos campos booleanos usados pelos filtros da API.
            campos_alergenos = {
                f"contem_{alergeno}": alergeno in item.alergenos
                for alergeno in ALERGENOS_VALIDOS
            }
            db.add(
                ItemCardapio(
                    cardapio_id=cardapio.id,
                    categoria=item.categoria,
                    tipo_dieta=item.tipo_dieta,
                    nome=item.nome,
                    **campos_alergenos,
                )
            )
            itens_processados += 1

    db.commit()
    return ImportacaoResultado(
        campus_id=campus.id,
        cardapios_processados=len(importacao.refeicoes),
        itens_processados=itens_processados,
    )


@router.get("/{cardapio_id}", response_model=CardapioRead)
def obter_cardapio(cardapio_id: int, db: Session = Depends(get_db)):
    cardapio = (
        db.query(Cardapio)
        .options(selectinload(Cardapio.itens))
        .filter(Cardapio.id == cardapio_id)
        .first()
    )
    if cardapio is None:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    return cardapio
