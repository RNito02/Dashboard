from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.orm import Session
from models import Empleados, Users, Vista_Vacaciones
from schemas import EmpleadoCreate, UserCreate, UserLogin, EmpleadoEdit
from database import SessionLocal, engine
from datetime import datetime
from datetime import date
import models

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Función para crear un empleado
def create_empleado(empleado: EmpleadoCreate, db: SessionLocal):
    # Verificar si el empleado ya existe
    existing_empleado = db.query(Empleados).filter(
        Empleados.num_nomina == empleado.num_nomina).first()
    if existing_empleado:
        raise HTTPException(status_code=400, detail="El empleado ya existe")

    # No es necesario aplicar strptime, ya que fecha_ingreso es una cadena
    fecha_ingreso = empleado.fecha_ingreso

    today = datetime.now().date()
    # Validar que la fecha_ingreso sea una fecha pasada
    if fecha_ingreso >= today:
        raise HTTPException(
            status_code=400, detail="La fecha de ingreso debe ser una fecha pasada")

    # Verificar si el jefe_directo existe
    if empleado.jefe_directo:
        jefe_directo = db.query(Empleados).filter(
            Empleados.num_nomina == empleado.jefe_directo).first()
        if not jefe_directo:
            raise HTTPException(
                status_code=400, detail="El jefe directo no existe")

    db_empleado = Empleados(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado


# Función para leer un empleado por número de nómina
def read_empleado(num_nomina: int, db: Session):
    empleado = db.query(Empleados).filter(
        Empleados.num_nomina == num_nomina).first()

    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Obtén el nombre del jefe directo si existe
    nombre_jefe_directo = None
    if empleado.jefe_directo is not None:
        jefe_directo = db.query(Empleados).filter(
            Empleados.num_nomina == empleado.jefe_directo).first()
        if jefe_directo:
            nombre_jefe_directo = jefe_directo.nombre

    # Crea un objeto EmpleadoCreate con el nombre del jefe directo
    empleado_data = {
        "num_nomina": empleado.num_nomina,
        "nombre": empleado.nombre,
        "jefe_directo": empleado.jefe_directo,
        "nombre_jefe_directo": nombre_jefe_directo,
        "email": empleado.email,
        "departamento": empleado.departamento,
        "fecha_ingreso": empleado.fecha_ingreso,
        "is_active": empleado.is_active
    }

    return empleado_data


# Editar un empleado
def edit_empleado(num_nomina: int, empleado_data: EmpleadoEdit, db: Session):
    # Buscar al empleado por su número de nómina
    empleado = db.query(Empleados).filter(
        Empleados.num_nomina == num_nomina).first()

    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Validar que la fecha de ingreso sea una fecha pasada
    fecha_ingreso = empleado_data.fecha_ingreso
    today = date.today()

    if fecha_ingreso >= today:
        raise HTTPException(
            status_code=400,
            detail="La fecha de ingreso debe ser una fecha pasada al día de hoy"
        )

    # Actualizar los campos del empleado con los nuevos valores
    for key, value in empleado_data.dict().items():
        setattr(empleado, key, value)

    db.commit()
    db.refresh(empleado)
    return empleado


# Eliminar un empleado
def delete_empleado(num_nomina: str, db: Session):
    db_empleado = db.query(Empleados).filter(
        Empleados.num_nomina == num_nomina).first()

    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Verificar si el empleado está ligado a un usuario
    associated_user = db.query(Users).filter(
        Users.num_nomina == num_nomina).first()

    if associated_user:
        raise HTTPException(
            status_code=400, detail="No se puede eliminar un empleado ligado a un usuario")

    db.delete(db_empleado)
    db.commit()
    return {"message": "Empleado eliminado exitosamente"}


# Función para crear un usuario
def create_user(user: UserCreate, db: Session):
    # Verificar si el empleado existe
    empleado = db.query(Empleados).filter(
        Empleados.num_nomina == user.num_nomina).first()
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Hash de la contraseña antes de almacenarla en la base de datos
    hashed_password = pwd_context.hash(user.hashed_password)

    db_user = Users(num_nomina=user.num_nomina,
                    hashed_password=hashed_password, rol_user=user.rol_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Función para leer un usuario por ID
def read_user(id: int, db: Session):
    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# Funcion para buscar todos los empleados
def get_all_empleados(db: Session):
    empleados = db.query(Empleados).all()
    return empleados


# Función para iniciar sesión
def login(user_data: UserLogin, db: Session):
    user = db.query(Users).filter(
        Users.num_nomina == user_data.num_nomina).first()

    if user is None:
        raise HTTPException(
            status_code=401, detail="Número de nómina incorrecto")

    # Verificar la contraseña hash
    if not user.verify_password(user_data.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}


# Funcion que busca la vista_vacaciones
def get_vacation_by_employee_id(num_nomina: int, db: Session, limit: int = 1):
    vacations = db.query(Vista_Vacaciones).filter(
        Vista_Vacaciones.num_nomina == num_nomina).limit(limit).first()

    if vacations is None:
        raise HTTPException(
            status_code=404, detail="Vacaciones no encontradas para el empleado")
    return vacations
