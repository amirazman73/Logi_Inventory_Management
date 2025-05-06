from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List

router = APIRouter()
get_db = database.SessionLocal

@router.post("/pallets/", response_model=schemas.PalletResponse)
def create_pallet(pallet_data: schemas.PalletCreate, db: Session = Depends(get_db)):
    # Create Pallet
    pallet = models.Pallet(
        pallet_code=pallet_data.pallet_code,
        created_at=pallet_data.created_at
    )
    db.add(pallet)
    db.commit()
    db.refresh(pallet)

    # Assign items to pallet
    items = db.query(models.StockItem).filter(models.StockItem.id.in_(pallet_data.item_ids)).all()
    for item in items:
        item.pallet_id = pallet.id
    db.commit()

    return {
        "id": pallet.id,
        "pallet_code": pallet.pallet_code,
        "created_at": pallet.created_at,
        "item_ids": [item.id for item in items]
    }

@router.get("/pallets/", response_model=List[schemas.PalletResponse])
def get_pallets(db: Session = Depends(get_db)):
    pallets = db.query(models.Pallet).all()
    result = []
    for pallet in pallets:
        item_ids = [item.id for item in pallet.items]
        result.append({
            "id": pallet.id,
            "pallet_code": pallet.pallet_code,
            "created_at": pallet.created_at,
            "item_ids": item_ids
        })
    return result