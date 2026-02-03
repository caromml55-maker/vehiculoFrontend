from sqlalchemy.orm import Session
import models

class VehiculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(models.Vehiculo).all()

    def find_by_placa(self, placa: str):
        return self.db.query(models.Vehiculo).filter(models.Vehiculo.placa == placa).first()

    def save(self, vehiculo: models.Vehiculo):
        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo