from fastapi import FastAPI
from routes import productos, users, autenticacion_basica, autenticacion_jwt,users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# con esto arranca el servidor: uvicorn main:app --reload

# Rutas
app.include_router(productos.router)
app.include_router(users.router)
app.include_router(autenticacion_basica.router)
app.include_router(autenticacion_jwt.router)
app.include_router(users_db.router)

# Recursos estaticos
app.mount("/static",StaticFiles(directory="static"),name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def root():
    return {"url": "www.google.comm"}