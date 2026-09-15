from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.campus import Campus
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInRead

router = APIRouter(prefix="/campi/{campus_id}/checkins", tags=["checkin"])


def _obter_campus_ou_404(campus_id: int, db: Session) -> None:
    if db.get(Campus, campus_id) is None:
        raise HTTPException(status_code=404, detail="Campus não encontrado")


@router.post("/", response_model=CheckInRead, status_code=201)
def registrar_checkin(campus_id: int, db: Session = Depends(get_db)):
    _obter_campus_ou_404(campus_id, db)
    checkin = CheckIn(campus_id=campus_id)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


@router.get("/", response_model=list[CheckInRead])
def listar_checkins(campus_id: int, db: Session = Depends(get_db)):
    _obter_campus_ou_404(campus_id, db)
    return (
        db.query(CheckIn)
        .filter(CheckIn.campus_id == campus_id)
        .order_by(CheckIn.criado_em.desc())
        .all()
    )
