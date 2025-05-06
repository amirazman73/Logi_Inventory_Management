from fastapi import FastAPI
from .routes import stock, pallets, item

app = FastAPI()

app.include_router(stock.router, prefix="/api")
app.include_router(pallets.router, prefix="/api")
app.include_router(item.router, prefix="/api")