from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    stock_entries = relationship("StockItem", back_populates="item")

class StockItem(Base):
    __tablename__ = "stock_items"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    date_of_collection = Column(DateTime)
    quantity = Column(Integer)
    status = Column(String, default="active") 
    location = Column(String)
    pallet_id = Column(Integer, ForeignKey("pallets.id"), nullable=True)

    item = relationship("Item", back_populates="stock_entries")
    pallet = relationship("Pallet", back_populates="items")

class Pallet(Base):
    __tablename__ = "pallets"
    id = Column(Integer, primary_key=True, index=True)
    pallet_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # New

    order = relationship("Order", back_populates="pallets")
    items = relationship("StockItem", back_populates="pallet")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_reference = Column(String)
    created_at = Column(DateTime)

    pallets = relationship("Pallet", back_populates="order")


class ImageUpload(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    pallet_id = Column(String)
    uploaded_at = Column(Date)

