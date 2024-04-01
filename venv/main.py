from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

database = {
    "ingresos": [],
    "egresos": []
}

class Ingreso(BaseModel):
    fecha: str
    descripcion: str
    valor: float
    categoria: str

class Egreso(BaseModel):
    fecha: str
    descripcion: str
    valor: float
    categoria: str

@app.post("/ingresos")
async def crear_ingreso(ingreso: Ingreso):
    database["ingresos"].append(ingreso)
    return {"mensaje": "Ingreso creado correctamente"}

@app.get("/ingresos")
async def listar_ingresos():
    return database["ingresos"]

@app.delete("/ingresos/{ingreso_id}")
async def eliminar_ingreso(ingreso_id: int):
    try:
        del database["ingresos"][ingreso_id]
        return {"mensaje": "Ingreso eliminado correctamente"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")

@app.post("/egresos")
async def crear_egreso(egreso: Egreso):
    database["egresos"].append(egreso)
    return {"mensaje": "Egreso creado correctamente"}

@app.get("/egresos")
async def listar_egresos():
    return database["egresos"]

@app.delete("/egresos/{egreso_id}")
async def eliminar_egreso(egreso_id: int):
    try:
        del database["egresos"][egreso_id]
        return {"mensaje": "Egreso eliminado correctamente"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Egreso no encontrado")

@app.get("/reporteBasico")
async def generar_reporte_basico():
    totalIngresos = sum(ingreso.valor for ingreso in database["ingresos"])
    totalEgresos = sum(egreso.valor for egreso in database["egresos"])
    balance = totalIngresos - totalEgresos
    return {
        "Total Ingresos": totalIngresos,
        "Total Egresos": totalEgresos,
        "Balance": balance
    }

@app.get("/reporteAmpliado")
async def generar_reporte_ampliado():
    categorias_ingresos = {}
    categorias_egresos = {}

    for ingreso in database["ingresos"]:
        if ingreso.categoria in categorias_ingresos:
            categorias_ingresos[ingreso.categoria] += ingreso.valor
        else:
            categorias_ingresos[ingreso.categoria] = ingreso.valor

    for egreso in database["egresos"]:
        if egreso.categoria in categorias_egresos:
            categorias_egresos[egreso.categoria] += egreso.valor
        else:
            categorias_egresos[egreso.categoria] = egreso.valor

    return {
        "Ingresos Por Categoria": categorias_ingresos,
        "Egresos Por Categoria": categorias_egresos
    }
