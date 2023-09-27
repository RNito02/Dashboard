from pydantic import BaseModel
from datetime import date


# Todo el schema de empleado
class EmpleadoCreate(BaseModel):
    num_nomina: int
    nombre: str
    email: str
    jefe_directo: int
    departamento: str
    fecha_ingreso: date
    is_active: bool


# Editar empleado
class EmpleadoEdit(BaseModel):
    nombre: str
    email: str
    jefe_directo: int
    departamento: str
    fecha_ingreso: date
    is_active: bool


# Todo el schema de User
class UserCreate(BaseModel):
    num_nomina: int
    rol_user: str
    hashed_password: str


# Todo el schema de Login
class UserLogin(BaseModel):
    num_nomina: int
    hashed_password: str


class View_Vacaciones_Schema(BaseModel):
    num_nomina: int
    nombre: str
    fecha_ingreso: date
    anios_servicio: int
    dias_vacaciones: int
