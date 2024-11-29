from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import SessionLocal, Producto, acelerometro, adc, bmp, ultrasonico

app = FastAPI()

origins = {
    "http://localhost:8000","http://localhost:5174"
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Producto).all()
    return products


class ProductoDTO(BaseModel):
    name: str
    description: str
    price: str
    weight: str

@app.get("/acelerometro")
def get_products(db: Session = Depends(get_db)):
    products = db.query(acelerometro).all()
    return products

class acelerometroDTO(BaseModel):
    id: int
    fecha: str
    valor_x : float
    valor_y : float
    valor_z : float

@app.get("/adc")
def get_products(db: Session = Depends(get_db)):
    products = db.query(adc).all()
    return products

class adcDTO(BaseModel):
    id: int
    fecha: str
    luz_valor : float
    voltaje : float

@app.get("/bmp")
def get_products(db: Session = Depends(get_db)):
    products = db.query(bmp).all()
    return products

class bmpDTO(BaseModel):
    id: int
    fecha: str
    temp: float
    presion : float
    altitud : float

@app.get("/ultrasonico")
def get_products(db: Session = Depends(get_db)):
    products = db.query(ultrasonico).all()
    return products

class ultrasonicoDT0(BaseModel):
    id: int
    fecha : str
    distancia_valor : float

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)