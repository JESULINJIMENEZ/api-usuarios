from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users  # Ajusta la ruta de importación según tu estructura

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permite solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir routers
app.include_router(users.router)
