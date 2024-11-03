from fastapi import APIRouter, HTTPException
from typing import List  # Asegúrate de incluir esta línea
from app.models.user import User
from app.database.fake_db import users_db

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: User):
    if any(existing_user["correo"] == user.correo for existing_user in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
    user.id = new_id
    users_db.append(user.dict())
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
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            del users_db[index]
            return
    raise HTTPException(status_code=404, detail="User not found")
