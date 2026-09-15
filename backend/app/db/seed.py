"""Popula o banco com dados de exemplo, para desbloquear testes de backend e frontend.

Uso (dentro do container do backend, via docker compose):
    docker compose exec backend python -m app.db.seed

Uso local (venv do backend ativado, com DATABASE_URL apontando pro Postgres e
a migração do Alembic já aplicada):
    cd backend
    python -m app.db.seed

Idempotente: remove o campus de seed (e tudo que depende dele, via cascade)
antes de inserir de novo, então pode ser rodado quantas vezes for preciso
sem duplicar dados.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import (
    Avaliacao,
    Campus,
    Cardapio,
    Categoria,
    ItemCardapio,
    TipoDieta,
    TipoRefeicao,
)

SEED_CAMPUS_NOME = "Gama"


def _limpar_seed_anterior(db: Session) -> None:
    campus_antigo = db.query(Campus).filter_by(nome=SEED_CAMPUS_NOME).one_or_none()
    if campus_antigo is not None:
        db.delete(campus_antigo)  # cascade cuida de cardápio -> itens/avaliações
        db.commit()


def _criar_campus(db: Session) -> Campus:
    campus = Campus(nome=SEED_CAMPUS_NOME)
    db.add(campus)
    db.flush()
    return campus


def _criar_cardapio(db: Session, campus: Campus) -> Cardapio:
    cardapio = Cardapio(
        campus_id=campus.id,
        data=date.today(),
        tipo_refeicao=TipoRefeicao.ALMOCO,
    )
    db.add(cardapio)
    db.flush()
    return cardapio


def _criar_itens(db: Session, cardapio: Cardapio) -> None:
    itens = [
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.PRATO_PRINCIPAL,
            tipo_dieta=TipoDieta.PADRAO,
            nome="Frango grelhado",
        ),
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.PRATO_PRINCIPAL,
            tipo_dieta=TipoDieta.VEGETARIANO_ESTRITO,
            nome="Grão-de-bico ao curry",
            contem_soja=True,
        ),
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.SALADA_1,
            tipo_dieta=TipoDieta.OVOLACTOVEGETARIANO,
            nome="Salada de alface e tomate",
        ),
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.GUARNICAO,
            tipo_dieta=TipoDieta.PADRAO,
            nome="Arroz branco",
        ),
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.SOBREMESA,
            tipo_dieta=TipoDieta.PADRAO,
            nome="Bolo de fubá",
            contem_gluten=True,
            contem_leite=True,
            contem_ovo=True,
        ),
        ItemCardapio(
            cardapio_id=cardapio.id,
            categoria=Categoria.FRUTA,
            tipo_dieta=TipoDieta.VEGETARIANO_ESTRITO,
            nome="Banana",
        ),
    ]
    db.add_all(itens)


def _criar_avaliacao(db: Session, cardapio: Cardapio) -> None:
    avaliacao = Avaliacao(
        cardapio_id=cardapio.id,
        nota=4,
        comentario="Comida boa, salada podia ter mais opções.",
    )
    db.add(avaliacao)


def _imprimir_resumo(db: Session, campus_id: int) -> None:
    campus = db.get(Campus, campus_id)
    print(f"Campus: {campus.nome} (id={campus.id})")
    for cardapio in campus.cardapios:
        print(f"  Cardápio {cardapio.data} - {cardapio.tipo_refeicao.value} (id={cardapio.id})")
        for item in cardapio.itens:
            print(f"    - [{item.categoria.value}/{item.tipo_dieta.value}] {item.nome}")
        for avaliacao in cardapio.avaliacoes:
            print(f"    Avaliação: nota={avaliacao.nota} comentário={avaliacao.comentario!r}")


def seed() -> None:
    db = SessionLocal()
    try:
        _limpar_seed_anterior(db)

        campus = _criar_campus(db)
        cardapio = _criar_cardapio(db, campus)
        _criar_itens(db, cardapio)
        _criar_avaliacao(db, cardapio)
        db.commit()

        _imprimir_resumo(db, campus.id)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
