from sqlalchemy.orm import Session
from repository import VehiculoRepository
import models, schemas

class VehiculoService:
    def __init__(self, db: Session):
        self.repo = VehiculoRepository(db)

    def get_all(self):
        return self.repo.find_all()
    
    def get_by_placa(self, placa: str):
        return self.repo.find_by_placa(placa)

    def create(self, datos: schemas.VehiculoCreate):
        # 1. Validación de Integridad: Placa debe tener guion en la 4ta posición (índice 3)
        # Ejemplo: AAA-123. índice 3 es el guion.
        if len(datos.placa) < 4 or datos.placa[3] != '-':
            raise ValueError("La placa debe contener un guion (-) en la cuarta posición.")

        # 2. Cálculo de Impuesto
        impuesto_base = datos.valor_comercial * 0.025
        
        # Regla: Recargo si es anterior a 2010 (+10% del base)
        if datos.fabricacion < 2010:
            impuesto_base += (impuesto_base * 0.10)
        
        # Regla: Beneficio si marca inicia con vocal (-$30)
        vocales = ['a', 'e', 'i', 'o', 'u']
        if datos.marca and datos.marca[0].lower() in vocales:
            impuesto_base -= 30.0
        
        # Resultado mínimo $0
        if impuesto_base < 0:
            impuesto_base = 0.0

        # 3. Generación de codigo_revision
        # 3 primeros caracteres de placa + longitud propietario + último dígito fabricacion
        parte_placa = datos.placa[:3]
        len_propietario = str(len(datos.propietario))
        ultimo_digito_anio = str(datos.fabricacion)[-1]
        
        codigo_generado = f"{parte_placa}{len_propietario}{ultimo_digito_anio}"

        # 4. Creación del Modelo
        nuevo_vehiculo = models.Vehiculo(
            placa=datos.placa,
            propietario=datos.propietario,
            marca=datos.marca,
            fabricacion=datos.fabricacion,
            valor_comercial=datos.valor_comercial,
            impuesto=impuesto_base,
            codigo_revision=codigo_generado
        )

        # 5. Persistencia vía Repositorio
        return self.repo.save(nuevo_vehiculo)