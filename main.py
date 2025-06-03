from fastapi import FastAPI

app = FastAPI()

# Simulación de una pequeña base de datos
fake_db = {
    1: {"name": "Producto 1", "precio": 10},
    2: {"name": "Producto 2", "precio": 20}
}

# GET


@app.get("/productos")
def get_productos():
    return {"productos": list(fake_db.values())}

# POST


@app.post("/productos")
def create_producto():
    new_id = max(fake_db) + 1
    fake_db[new_id] = {"name": f"Producto {new_id}", "precio": 15}
    return {"mensaje": "Producto creado", "producto": fake_db[new_id]}

# PUT


@app.put("/productos/{producto_id}")
def update_producto(producto_id: int):
    if producto_id in fake_db:
        fake_db[producto_id] = {
            "name": f"Producto {producto_id}", "precio": 99}
        return {"mensaje": "Producto reemplazado", "producto": fake_db[producto_id]}
    return {"error": "Producto no encontrado"}

# PATCH


@app.patch("/productos/{producto_id}")
def patch_producto(producto_id: int):
    if producto_id in fake_db:
        fake_db[producto_id]["precio"] = 50
        return {"mensaje": "Producto modificado parcialmente", "producto": fake_db[producto_id]}
    return {"error": "Producto no encontrado"}

# DELETE


@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int):
    if producto_id in fake_db:
        eliminado = fake_db.pop(producto_id)
        return {"mensaje": "Producto eliminado", "producto": eliminado}
    return {"error": "Producto no encontrado"}

# HEAD


@app.head("/productos")
def head_productos():
    return {}

# OPTIONS


@app.options("/productos")
def options_productos():
    return {
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    }
