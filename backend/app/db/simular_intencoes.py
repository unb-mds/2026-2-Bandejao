"""Geração e remoção explícitas de intenções para demonstrações."""

import argparse
import json
import sys
from datetime import date
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Cardapio, Intencao, TipoRefeicao


def _cardapio(db: Session, campus_id: int, data: date, tipo_refeicao: TipoRefeicao) -> Cardapio:
    cardapio = db.query(Cardapio).filter_by(
        campus_id=campus_id, data=data, tipo_refeicao=tipo_refeicao
    ).one_or_none()
    if cardapio is None:
        raise ValueError("Refeição não encontrada para o campus, data e refeição informados.")
    return cardapio


def criar_simuladas(
    db: Session, campus_id: int, data: date, tipo_refeicao: TipoRefeicao, quantidade: int
) -> int:
    """Acrescenta um lote atômico com novas identidades UUID v4."""
    if type(quantidade) is not int or not 1 <= quantidade <= 10000:
        raise ValueError("quantidade deve ser um inteiro entre 1 e 10000.")
    try:
        cardapio = _cardapio(db, campus_id, data, tipo_refeicao)
        db.add_all([
            Intencao(cardapio_id=cardapio.id, identidade=uuid4(), ativa=True, simulada=True)
            for _ in range(quantidade)
        ])
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return quantidade


def remover_simuladas(db: Session, campus_id: int, data: date, tipo_refeicao: TipoRefeicao) -> int:
    """Remove somente intenções simuladas da refeição cadastrada selecionada."""
    try:
        cardapio = _cardapio(db, campus_id, data, tipo_refeicao)
        quantidade = db.query(Intencao).filter_by(
            cardapio_id=cardapio.id, simulada=True
        ).delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return quantidade


def _positivo(texto: str) -> int:
    try:
        valor = int(texto)
    except ValueError as erro:
        raise argparse.ArgumentTypeError("Informe um inteiro positivo.") from erro
    if valor <= 0:
        raise argparse.ArgumentTypeError("Informe um inteiro positivo.")
    return valor


def _quantidade(texto: str) -> int:
    valor = _positivo(texto)
    if valor > 10000:
        raise argparse.ArgumentTypeError("quantidade deve estar entre 1 e 10000.")
    return valor


def _data_iso(texto: str) -> date:
    try:
        valor = date.fromisoformat(texto)
        if valor.isoformat() != texto:
            raise ValueError
    except ValueError as erro:
        raise argparse.ArgumentTypeError("Informe uma data válida no formato YYYY-MM-DD.") from erro
    return valor


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="operacao", required=True)
    for operacao in ("criar", "remover"):
        comando = comandos.add_parser(operacao)
        comando.add_argument("--campus-id", type=_positivo, required=True)
        comando.add_argument("--data", type=_data_iso, required=True)
        comando.add_argument("--refeicao", choices=[tipo.value for tipo in TipoRefeicao], required=True)
        if operacao == "criar":
            comando.add_argument("--quantidade", type=_quantidade, required=True)
    args = parser.parse_args(argv)
    try:
        with SessionLocal() as db:
            seletores = (db, args.campus_id, args.data, TipoRefeicao(args.refeicao))
            if args.operacao == "criar":
                quantidade = criar_simuladas(*seletores, args.quantidade)
            else:
                quantidade = remover_simuladas(*seletores)
    except ValueError as erro:
        print(str(erro), file=sys.stderr)
        return 1
    except SQLAlchemyError:
        print("Falha no banco de dados; operação não concluída.", file=sys.stderr)
        return 1
    print(json.dumps({
        "operacao": args.operacao,
        "campus_id": args.campus_id,
        "data": args.data.isoformat(),
        "refeicao": args.refeicao,
        "quantidade": quantidade,
        "dados_simulados": True,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
