from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int]  # Cambia a Optional si no se envía al crear
    nombre: str
    username: str
    correo: EmailStr
