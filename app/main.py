from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import schemas, service, database, models

app = FastAPI(title="Sistema Matrícula Vehicular")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

def get_vehiculo_service(db: Session = Depends(database.get_db)):
    return service.VehiculoService(db)

@app.get("/api/vehiculos", response_model=List[schemas.Vehiculo])
def read_vehiculos(srv: service.VehiculoService = Depends(get_vehiculo_service)):
    return srv.get_all()

@app.post("/api/vehiculos", response_model=schemas.Vehiculo, status_code=status.HTTP_201_CREATED)
def create_vehiculo(vehiculo: schemas.VehiculoCreate, srv: service.VehiculoService = Depends(get_vehiculo_service)):
    try:
        return srv.create(vehiculo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Error al procesar: {str(e)}")

@app.get("/api/vehiculos/{placa}", response_model=schemas.Vehiculo)
def read_vehiculo_by_placa(placa: str, srv: service.VehiculoService = Depends(get_vehiculo_service)):
    db_vehiculo = srv.get_by_placa(placa)
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

