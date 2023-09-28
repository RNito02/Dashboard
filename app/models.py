from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from database import Base
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# actualizado
class Empleados(Base):
    __tablename__ = "empleados"

    num_nomina = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    jefe_directo = Column(Integer, ForeignKey('empleados.num_nomina'))
    nombre_jefe_directo = relationship('Empleados', remote_side=[num_nomina])
    departamento = Column(String, index=True)
    fecha_ingreso = Column(Date, index=True)
    is_active = Column(Boolean, default=True)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    num_nomina = Column(Integer, ForeignKey("empleados.num_nomina"))
    rol_user = Column(String, index=True)
    hashed_password = Column(String, index=True)

    # Método para verificar la contraseña

    def verify_password(self, hashed_password: str):
        return pwd_context.verify(hashed_password, self.hashed_password)


class Vista_Vacaciones(Base):
    __tablename__ = "vista_vacaciones"

    # id = Column(Integer)
    num_nomina = Column(Integer, primary_key=True)
    nombre = Column(String)
    fecha_ingreso = Column(Date)
    anios_servicio = Column(Integer)
    dias_vacaciones = Column(Integer)


class Config_vacaciones(Base):
    __tablename__ = "config_vacaciones"

    anios_servicio = Column(Integer, primary_key=True)
    dias_vacaciones = Column(Integer)


class Solicitudes(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True)
    num_nomina = Column(Integer, ForeignKey("empleados.num_nomina"))
    fecha_solicitud = Column(Date)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    dias_solicitados = Column(Integer)
    fecha_reincorporacion = Column(Date)
