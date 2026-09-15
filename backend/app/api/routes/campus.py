from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.campus import Campus
from app.schemas.campus import CampusRead

router = APIRouter(prefix="/campi", tags=["campus"])


@router.get("/", response_model=list[CampusRead])
def listar_campi(db: Session = Depends(get_db)):
    return db.query(Campus).order_by(Campus.nome).all()


@router.get("/{campus_id}", response_model=CampusRead)
def obter_campus(campus_id: int, db: Session = Depends(get_db)):
    campus = db.get(Campus, campus_id)
    if campus is None:
        raise HTTPException(status_code=404, detail="Campus não encontrado")
    return campus