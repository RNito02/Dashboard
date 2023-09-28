from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from crud import create_empleado, read_empleado, create_user, read_user, login, edit_empleado, delete_empleado, get_vacation_by_employee_id, get_all_empleados
from schemas import EmpleadoCreate, UserCreate, UserLogin, EmpleadoEdit, View_Vacaciones_Schema, LeerEmpleados
from database import SessionLocal, engine
from models import Empleados, Users, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI()


# Configura el middleware CORS
origins = [
    "http://localhost",
    "http://192.168.105.93:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear un nuevo empleado
@app.post("/add_empleado/", response_model=EmpleadoCreate)
def create_employee(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    return create_empleado(empleado, db)


# Buscar un empleado por su num de nomina
@app.get("/search_empleado/{num_nomina}", response_model=LeerEmpleados)
def read_employee(num_nomina: int, db: Session = Depends(get_db)):
    empleado_data = read_empleado(num_nomina, db)
    if not empleado_data:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado_data


# Buscar todos los empleados
@app.get("/get_all_empleados")
def get_all_employees(db: Session = Depends(get_db)):
    empleados = get_all_empleados(db)
    return empleados


# Editar a un empleado por su PK
@app.put("/edit_empleado/{num_nomina}", response_model=EmpleadoCreate)
def update_employee(num_nomina: int, empleado_data: EmpleadoEdit, db: Session = Depends(get_db)):
    return edit_empleado(num_nomina, empleado_data, db)


# Eliminar empleado
@app.delete("/delete_empleados/{num_nomina}")
def delete_employee(num_nomina: int, db: Session = Depends(get_db)):
    return delete_empleado(num_nomina, db)


# Crear un usuario nuevo
@app.post("/create_users/", response_model=UserCreate)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


# buscar un usuario por su PK
@app.get("/buscar_user/{id}", response_model=UserCreate)
def read_user_by_id(id: int, db: Session = Depends(get_db)):
    return read_user(id, db)


# Acceso a Login
@app.post("/login/")
def user_login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login(user_data, db)


# Hace la consulta a las vacaciones
@app.get("/view_vacaciones/{num_nomina}", response_model=View_Vacaciones_Schema)
def query_vacaciones(num_nomina: int, db: Session = Depends(get_db)):
    return get_vacation_by_employee_id(num_nomina, db)
