from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Producto, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Productos con FastAPI y MySQL")

# Dependencia de base de datos


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/productos")
def get_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return {"productos": [{"id": p.id, "name": p.name, "precio": p.precio} for p in productos]}


@app.post("/productos")
def create_producto(db: Session = Depends(get_db)):
    nuevo = Producto(name="Producto nuevo", precio=25.0)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Producto creado", "producto": {"id": nuevo.id, "name": nuevo.name, "precio": nuevo.precio}}


@app.put("/productos/{producto_id}")
def update_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.name = f"Producto {producto_id}"
    producto.precio = 99.0
    db.commit()
    return {"mensaje": "Producto actualizado", "producto": {"id": producto.id, "name": producto.name, "precio": producto.precio}}


@app.patch("/productos/{producto_id}")
def patch_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.precio = 50.0
    db.commit()
    return {"mensaje": "Producto modificado parcialmente", "producto": {"id": producto.id, "name": producto.name, "precio": producto.precio}}


@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado", "producto": {"id": producto.id, "name": producto.name, "precio": producto.precio}}


@app.head("/productos")
def head_productos():
    return {}


@app.options("/productos")
def options_productos():
    return {
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    }
