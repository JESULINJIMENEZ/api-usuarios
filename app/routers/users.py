import json
import os
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User

router = APIRouter()
file_path = "users.json"

# Función para cargar usuarios desde el archivo
def load_users():
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

# Función para guardar usuarios en el archivo
def save_users(users):
    with open(file_path, "w") as file:
        json.dump(users, file)

# Cargar los usuarios al inicio
users_db = load_users()

@router.post("/users/", response_model=User)
def create_user(user: User):
    if any(existing_user["correo"] == user.correo for existing_user in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
    user.id = new_id
    users_db.append(user.dict())
    save_users(users_db)  # Guardar cambios en el archivo
    return user

@router.get("/users/", response_model=List[User])
def read_users():
    return users_db

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    for index, existing_user in enumerate(users_db):
        if existing_user["id"] == user_id:
            if any(existing_user["correo"] == user.correo for existing_user in users_db if existing_user["id"] != user_id):
                raise HTTPException(status_code=400, detail="Email already registered")
                
            user.id = user_id
            users_db[index] = user.dict()
            save_users(users_db)  # Guardar cambios en el archivo
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            del users_db[index]
            save_users(users_db)  # Guardar cambios en el archivo
            return
    raise HTTPException(status_code=404, detail="User not found")
