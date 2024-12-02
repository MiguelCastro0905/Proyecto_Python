from pydantic import BaseModel
from fastapi import APIRouter, status, HTTPException
import hashlib 
from conexion import cursor, mydb
import mysql.connector


regisRouter = APIRouter()

class registro_usuario(BaseModel):
    id: int
    correo: str
    contrasena: str

@regisRouter.post("/registro", status_code=status.HTTP_201_CREATED)
def insert_user(user:registro_usuario):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(user.contrasena.encode()).hexdigest()

    insert_query = """
    INSERT INTO registro_usuario ( id, correo, contrasena)
    VALUES (%s, %s, %s)
    """
    values = (user.id, user.correo, hashed_password)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}