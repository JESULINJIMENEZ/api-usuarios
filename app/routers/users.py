from fastapi import APIRouter, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

# Configuración de MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["user_db"]
users_collection = db["users"]

class User(BaseModel):
    id: Optional[int]  # Cambia a Optional
    nombre: str
    username: str
    correo: EmailStr

@router.post("/users/", response_model=User)
async def create_user(user: User):
    # Buscar el máximo ID actual para asignar uno nuevo
    max_user = await users_collection.find_one(sort=[("id", -1)])  # Encuentra el usuario con el ID más alto
    new_id = (max_user['id'] + 1) if max_user else 1  # Asignar nuevo ID
    
    new_user = {
        "id": new_id,
        "nombre": user.nombre,
        "username": user.username,
        "correo": user.correo
    }
    
    await users_collection.insert_one(new_user)
    return new_user

@router.get("/users/", response_model=List[User])
async def read_users():
    users = []
    async for user in users_collection.find():
        user["id"] = user["id"]  # Asegúrate de que el ID se maneje como int
        users.append(user)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):  # Cambiar a int
    user = await users_collection.find_one({"id": user_id})  # Buscar por ID numérico
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):  # Cambiar a int
    existing_user = await users_collection.find_one({"id": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualiza el usuario en la base de datos
    await users_collection.update_one({"id": user_id}, {"$set": user.dict()})
    return {**user.dict(), "id": user_id}

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):  # Cambiar a int
    result = await users_collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
