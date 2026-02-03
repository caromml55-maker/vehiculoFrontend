from pydantic import BaseModel
# Base común
class VehiculoBase(BaseModel):
    placa: str
    propietario: str
    marca: str
    fabricacion: int
    valor_comercial: float

# Para creación (Input)
class VehiculoCreate(VehiculoBase):
    pass

# Para respuesta (Output) - Incluye los calculados
class Vehiculo(VehiculoBase):
    impuesto: float
    codigo_revision: str

    class Config:
        from_attributes = True