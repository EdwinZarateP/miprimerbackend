from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITMO = "HS256"
DURACION_TOKEN = 1
SECRET = "ASJJEEQFDA324356Y6RJHFGDFSD"


router = APIRouter(prefix="/jwtauth", 
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})
# con esto arranca el servidor: uvicorn autenticacion_jwt:app --reload

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool 

class UserDB(User):
    clave: str

base_usuarios = {  # esto un diccionario que contiene datos de usuarios,
    # donde la clave es el nombre de usuario y el valor es
    # otro diccionario con la información del usuario.
    "edwin": {
        "username": "edwin",
        "full_name": "Edwin Zarate",
        "email": "emzp",
        "disabled": False,
        "clave": "$2a$12$DOcsjjssDY8Y0p0Iu2ABFupgMKvjvJ4djwE80orX7A5nEMB8imrsG"
    },
    "laura": {
        "username": "laura",
        "full_name": "Laura Navarro",
        "email": "lvno",
        "disabled": False,
        "clave": "$2a$12$v4YT7hvi6d2puR.UrJT0..DswIYpCPmiul7UXrYj1wgZuuBiPKDZ6"
    }
}

def buscarusuarioDB(username: str):
    if username in base_usuarios:
        return UserDB(**base_usuarios[username])
    return None

def buscarusuario(username: str):
    if username in base_usuarios:
        return User(**base_usuarios[username])
    return None

async def usuario_autenticado(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='Credenciales invalidas',
                              headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    usuario = buscarusuario(username)
    if usuario is None:
        raise exception

    return usuario

async def usuario_actual(usuario: User = Depends(usuario_autenticado)):
    if usuario.disabled:
        print("hola3")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Usuario inactivo')
    return usuario

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario_bd = base_usuarios.get(form.username)  # .get(form.username) es un método de diccionario
    # en Python que intenta obtener el valor asociado con la clave form.username en el diccionario base_usuarios.
    if not usuario_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='El usuario no es correcto')

    usuario = buscarusuarioDB(form.username)

    if not crypt.verify(form.password, usuario.clave):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='la clave no es correcta')

    expiracion_token = datetime.now(timezone.utc) + timedelta(minutes=DURACION_TOKEN)

    access_token = {"sub": usuario.username,
                    "exp": expiracion_token}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITMO), "token_type": "bearer"}

@router.get("/usuarios/yo")
async def yo(usuario: User = Depends(usuario_actual)):
    return usuario
