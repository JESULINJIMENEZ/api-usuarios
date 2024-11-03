from fastapi import FastAPI
from app.middlewares.cors import setup_cors
from app.routers import users

app = FastAPI()

# Configuración de CORS
setup_cors(app)

# Incluir routers
app.include_router(users.router)
