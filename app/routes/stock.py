from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from typing import Optional

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/stock/", response_model=schemas.StockResponse)
def create_stock_item(item: schemas.StockCreate, db: Session = Depends(get_db)):
    db_item = models.StockItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/stock/", response_model=list[schemas.StockResponse])
def get_stock_items(location: Optional[str] = None, db: Session = Depends(get_db)): 
    query = db.query(models.StockItem)
    if location:
        query = query.filter(models.StockItem.location == location)
    return query.all()

@router.put("/stock/{stock_id}", response_model=schemas.StockResponse)
def update_stock_item(
    stock_id: int,
    updated_data: schemas.StockUpdate,
    db: Session = Depends(get_db)
):
    stock_item = db.query(models.StockItem).filter(models.StockItem.id == stock_id).first()

    if not stock_item:
        raise HTTPException(status_code=404, detail="Stock item not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(stock_item, key, value)

    db.commit()
    db.refresh(stock_item)
    return stock_item


@router.get("/stock/active", response_model=list[schemas.StockResponse])
def get_active_stock_items(db: Session = Depends(get_db)):
    return db.query(models.StockItem).filter(models.StockItem.status == "active").all()
